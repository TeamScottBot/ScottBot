"""
Usage:
    python3 visualize_path.py /ScottBot/maps/my_house7.yaml 125 95 55 85

Saves result as path_preview.pgm next to the map file.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from astar import load_map, inflate_grid, astar, simplify_path, path_to_commands


def main():
    if len(sys.argv) < 6:
        print("Usage: python3 visualize_path.py <map.yaml> <start_row> <start_col> <goal_row> <goal_col> [inflate_r]")
        sys.exit(1)

    map_file = sys.argv[1]
    start = (int(sys.argv[2]), int(sys.argv[3]))
    goal = (int(sys.argv[4]), int(sys.argv[5]))
    radius = int(sys.argv[6]) if len(sys.argv) > 6 else 2

    map_data = load_map(map_file)
    grid = map_data["grid"]
    rows = len(grid)
    cols = len(grid[0])
    print(f"Map: {rows}x{cols}, start={start}, goal={goal}, inflate_r={radius}")

    planning_grid = inflate_grid(grid, radius)

    print(f"Start cell value (raw): {grid[start[0]][start[1]]}")
    print(f"Start cell value (inflated): {planning_grid[start[0]][start[1]]}")
    print(f"Goal cell value (raw): {grid[goal[0]][goal[1]]}")
    print(f"Goal cell value (inflated): {planning_grid[goal[0]][goal[1]]}")

    out = []
    for r in range(rows):
        row = []
        for c in range(cols):
            if planning_grid[r][c] == 1:
                row.append(0)
            else:
                row.append(200)
        out.append(row)

    for dr in range(-3, 4):
        for dc in range(-3, 4):
            sr, sc = start[0] + dr, start[1] + dc
            gr, gc = goal[0] + dr, goal[1] + dc
            if 0 <= sr < rows and 0 <= sc < cols:
                out[sr][sc] = 255
            if 0 <= gr < rows and 0 <= gc < cols:
                out[gr][gc] = 50

    try:
        path = astar(planning_grid, start, goal)
    except ValueError as e:
        print(f"A* error: {e}")
        path = None

    if path:
        simplified = simplify_path(path)
        commands = path_to_commands(path)
        print(f"Path: {len(path)} cells, {len(simplified)} waypoints, {len(commands)} commands")
        for cmd_type, value in commands:
            unit = "°" if cmd_type == "TURN" else "m"
            print(f"  {cmd_type:>7s}  {value:>8.3f}{unit}")
        for r, c in path:
            out[r][c] = 120
    else:
        print("No path found — check preview to adjust coordinates")

    out_path = os.path.join(os.path.dirname(map_file), "path_preview.pgm")
    with open(out_path, "wb") as f:
        f.write(f"P5\n{cols} {rows}\n255\n".encode())
        for row in out:
            f.write(bytes(row))
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
