from __future__ import annotations

import heapq
import math
import os
import yaml
from typing import Dict, List, Optional, Tuple

Cell = Tuple[int, int]
Command = Tuple[str, float]

# all 8 neighbors as (row_delta, col_delta)
DIRECTIONS: List[Cell] = [
    (-1,  0),  # N
    (-1,  1),  # NE
    ( 0,  1),  # E
    ( 1,  1),  # SE
    ( 1,  0),  # S
    ( 1, -1),  # SW
    ( 0, -1),  # W
    (-1, -1),  # NW
]

# costs
_CARD: float = 1.0
_DIAG: float = math.sqrt(2)

# maps a (dr, dc) direction to the heading angle in degrees
_DIR_TO_HEADING: Dict[Cell, float] = {
    (-1,  0): 90.0,
    (-1,  1): 45.0,
    ( 0,  1): 0.0,
    ( 1,  1): 315.0,
    ( 1,  0): 270.0,
    ( 1, -1): 225.0,
    ( 0, -1): 180.0,
    (-1, -1): 135.0,
}

# Heuristic for 8-direction grids
def _octile(a: Cell, b: Cell) -> float:
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (_DIAG - _CARD) * min(dx, dy)


def astar(
    grid: List[List[int]],
    start: Cell,
    goal: Cell,
) -> Optional[List[Cell]]:
    # run A* on the grid
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # validate start and goal
    for tag, (r, c) in [("Start", start), ("Goal", goal)]:
        if not (0 <= r < rows and 0 <= c < cols):
            raise ValueError(f"{tag} {(r, c)} is out of bounds ({rows}x{cols})")
        if grid[r][c] != 0:
            raise ValueError(f"{tag} {(r, c)} is inside an obstacle")

    if start == goal:
        return [start]

    # priority queue entries
    open_heap: list = []
    cnt = 0
    heapq.heappush(open_heap, (_octile(start, goal), cnt, 0.0, start))

    came_from: Dict[Cell, Cell] = {}
    best_g: Dict[Cell, float] = {start: 0.0}

    while open_heap:
        _f, _cnt, g, cur = heapq.heappop(open_heap)

        if cur == goal:
            # rebuild the path
            path: List[Cell] = [cur]
            while cur in came_from:
                cur = came_from[cur]
                path.append(cur)
            path.reverse()
            return path

        # skip if we already found a better route
        if g > best_g.get(cur, math.inf):
            continue

        cr, cc = cur
        for dr, dc in DIRECTIONS:
            nr, nc = cr + dr, cc + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] != 0:
                continue

            # don't cut corners
            if dr != 0 and dc != 0:
                if grid[cr + dr][cc] != 0 or grid[cr][cc + dc] != 0:
                    continue

            ng = g + (_DIAG if (dr != 0 and dc != 0) else _CARD)

            if ng < best_g.get((nr, nc), math.inf):
                came_from[(nr, nc)] = cur
                best_g[(nr, nc)] = ng
                cnt += 1
                heapq.heappush(
                    open_heap,
                    (ng + _octile((nr, nc), goal), cnt, ng, (nr, nc)),
                )

    return None


def inflate_grid(
    grid: List[List[int]],
    radius_cells: int,
) -> List[List[int]]:
    # grow obstacles outward
    if radius_cells <= 0:
        return [row[:] for row in grid]

    rows, cols = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    rsq = radius_cells * radius_cells

    # mark everything within radius as blocked
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                continue
            for dr in range(-radius_cells, radius_cells + 1):
                for dc in range(-radius_cells, radius_cells + 1):
                    if dr * dr + dc * dc > rsq:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        out[nr][nc] = 1
    return out


def simplify_path(path: List[Cell]) -> List[Cell]:
    # drop intermediate waypoints that are just going straight
    if len(path) <= 2:
        return list(path)

    result: List[Cell] = [path[0]]
    for i in range(1, len(path) - 1):
        d_prev = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        d_next = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
        if d_prev != d_next:
            result.append(path[i])
    result.append(path[-1])
    return result


def path_to_commands(
    path: List[Cell],
    cell_size: float = 0.05,
    initial_heading: float = 90.0,
) -> List[Command]:
    if not path or len(path) < 2:
        return []

    cmds: List[Command] = []
    heading = initial_heading
    i = 1

    while i < len(path):
        dr = path[i][0] - path[i - 1][0]
        dc = path[i][1] - path[i - 1][1]
        required = _DIR_TO_HEADING[(dr, dc)]

        # shortest turn to face the right direction
        turn = (required - heading + 180.0) % 360.0 - 180.0
        if abs(turn) > 0.01:
            cmds.append(("TURN", round(turn, 1)))
            heading = required

        # merge consecutive steps in the same direction into one FORWARD
        diag = dr != 0 and dc != 0
        step = cell_size * _DIAG if diag else cell_size
        dist = 0.0

        while i < len(path):
            d = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
            if d == (dr, dc):
                dist += step
                i += 1
            else:
                break

        cmds.append(("FORWARD", round(dist, 4)))

    return cmds



def grid_to_world(
    cell: Cell,
    resolution: float,
    origin: Tuple[float, float] = (0.0, 0.0),
    grid_height: int = 0,
) -> Tuple[float, float]:
    # (row, col) -> (x, y) in metres
    row, col = cell
    x = origin[0] + (col + 0.5) * resolution
    y = origin[1] + (grid_height - row - 0.5) * resolution
    return (x, y)


def world_to_grid(
    point: Tuple[float, float],
    resolution: float,
    origin: Tuple[float, float] = (0.0, 0.0),
    grid_height: int = 0,
) -> Cell:
    col = int((point[0] - origin[0]) / resolution)
    row = grid_height - 1 - int((point[1] - origin[1]) / resolution)
    return (row, col)

# load a map YAML. ROS standard or custom embedded grid
def load_map(filepath: str) -> dict:
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    if "image" in data:
        return _load_image_map(filepath, data)

    if "grid" in data:
        data.setdefault("origin", [0.0, 0.0])
        data["grid_height"] = len(data["grid"])
        return data

    raise KeyError("Map YAML must have either an 'image' or 'grid' key")


def _load_image_map(yaml_path: str, data: dict) -> dict:
    try:
        import cv2
    except ImportError:
        raise ImportError(
        )

    image_path = data["image"]
    if not os.path.isabs(image_path):
        image_path = os.path.join(os.path.dirname(yaml_path), image_path)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read map image: {image_path}")

    resolution = data["resolution"]
    origin = list(data.get("origin", [0.0, 0.0, 0.0]))[:2]
    negate = data.get("negate", 0)
    occupied_thresh = data.get("occupied_thresh", 0.65)
    free_thresh = data.get("free_thresh", 0.25)

    # convert pixel brightness to occupancy (0 = free, 1 = wall)
    img_f = img.astype(float)
    if negate:
        occ = img_f / 255.0
    else:
        occ = (255.0 - img_f) / 255.0

    rows, cols = img.shape
    grid: List[List[int]] = []
    for r in range(rows):
        row: List[int] = []
        for c in range(cols):
            if occ[r, c] < free_thresh:
                # free
                row.append(0)
            else:
                # occupied or unknown
                row.append(1)
        grid.append(row)

    return {
        "grid": grid,
        "resolution": resolution,
        "origin": origin,
        "grid_height": rows,
    }
