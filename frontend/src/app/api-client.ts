const API_BASE = "https://api.qhgill2.workers.dev";

export const ROBOT_ID = "default";

export type OrderStatus =
  | "idle"
  | "moving_to_pickup"
  | "waiting_for_pickup"
  | "moving_to_dropoff"
  | "waiting_for_dropoff"
  | "delivered";

export type OrderState = {
  id?: string;
  pickupLocation: string;
  dropoffLocation: string;
  status: OrderStatus;
};

export async function initRobot(): Promise<{ robotId: string }> {
  const res = await fetch(`${API_BASE}/orders`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to init robot");
  return res.json();
}

export async function startOrder(
  robotId: string,
  body: { pickupLocation: string; dropoffLocation: string }
): Promise<{ orderId: string }> {
  const res = await fetch(`${API_BASE}/orders/${robotId}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { error?: string }).error ?? "Failed to start order");
  }
  return res.json();
}

export async function getOrderStatus(
  robotId: string
): Promise<{ status: "idle" } | OrderState> {
  const res = await fetch(`${API_BASE}/orders/${robotId}/status`);
  if (!res.ok) throw new Error("Failed to get order status");
  return res.json();
}

export async function updateOrderStatus(
  robotId: string,
  body: { status: OrderStatus; pickupLocation: string; dropoffLocation: string }
): Promise<OrderState> {
  const res = await fetch(`${API_BASE}/orders/${robotId}/update`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error("Failed to update order");
  return res.json();
}

export async function deleteOrder(robotId: string): Promise<{ ok: boolean }> {
  const res = await fetch(`${API_BASE}/orders/${robotId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete order");
  return res.json();
}

export function getOrderWebSocketUrl(robotId: string): string {
  const base = API_BASE.replace(/^http/, "ws");
  return `${base}/orders/${robotId}/ws`;
}
