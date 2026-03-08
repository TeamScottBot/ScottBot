import { OrderState } from "../types"

const WS_TAG = "order-client"

export class OrderDO {
  state: DurableObjectState

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(req: Request) {
    const url = new URL(req.url)
    // Accept both /ws (when worker rewrites URL) and .../ws (when worker forwards original request)
    if (url.pathname === "/ws" || url.pathname.endsWith("/ws")) {
      const pair = new WebSocketPair()
      const [client, server] = [pair[0], pair[1]]

      // Tag so we can retrieve connections via getWebSockets() after hibernation
      this.state.acceptWebSocket(server, [WS_TAG])

      // Send welcome so the client gets a message immediately and confirms the pipe works
      server.send(JSON.stringify({ type: "connected", message: "Order server ready" }))

      return new Response(null, {
        status: 101,
        webSocket: client
      })
    }

    if (url.pathname === "/init") {
      await this.state.storage.put("status", "idle")
      return new Response("ok")
    }

    if (url.pathname === "/start") {
      const currentStatus = await this.state.storage.get<string>("status")
      if (currentStatus && currentStatus !== "idle") {
        return new Response("robot is not idle", { status: 400 })
      }

      const { id, pickupLocation, dropoffLocation } = await req.json<OrderState>()
      await this.state.storage.put("order", { id, pickupLocation, dropoffLocation })
      await this.state.storage.put("status", "moving_to_pickup")

      const orderData = {
        orderId: id,
        pickupLocation,
        dropoffLocation,
        status: "moving_to_pickup"
      }
      this.broadcastToClients(orderData)

      return new Response("ok")
    }

    if (url.pathname === "/status") {
      const status = await this.state.storage.get<string>("status")
      const order = await this.state.storage.get<OrderState>("order")

      if (status === "idle" || !order) {
        return Response.json({ status: "idle" })
      }

      return Response.json({
        id: order.id,
        pickupLocation: order.pickupLocation,
        dropoffLocation: order.dropoffLocation,
        status
      })
    }

    if (url.pathname === "/update") {
      const { status } = await req.json<{ status: string }>()
      const order = await this.state.storage.get<OrderState>("order")

      if (!order) {
        return new Response("no active order", { status: 404 })
      }

      await this.state.storage.put("status", status)

      this.broadcastToClients({
        orderId: order.id,
        pickupLocation: order.pickupLocation,
        dropoffLocation: order.dropoffLocation,
        status
      })

      return Response.json({
        id: order.id,
        pickupLocation: order.pickupLocation,
        dropoffLocation: order.dropoffLocation,
        status
      })
    }

    if (url.pathname === "/emergency-stop") {
      this.broadcastToClients({ type: "emergency_stop" })
      return Response.json({ ok: true })
    }

    if (url.pathname === "/delete") {
      const order = await this.state.storage.get<OrderState>("order")
      await this.state.storage.deleteAll()

      this.broadcastToClients({
        orderId: order?.id ?? "unknown",
        pickupLocation: order?.pickupLocation ?? "unknown",
        dropoffLocation: order?.dropoffLocation ?? "unknown",
        status: "idle"
      })

      return Response.json({ deleted: true })
    }

    return new Response("not found", { status: 404 })
  }

  private broadcastToClients(data: unknown) {
    const message = JSON.stringify(data)
    // Use getWebSockets() so we see connections after hibernation; in-memory Set is lost when DO is evicted
    const clients = this.state.getWebSockets(WS_TAG)
    for (const ws of clients) {
      try {
        ws.send(message)
      } catch {
        // Runtime will remove closed sockets from getWebSockets()
      }
    }
  }

  async webSocketMessage(_ws: WebSocket, _message: ArrayBuffer | string) {
    // Optional: handle incoming messages from Pi
  }

  async webSocketClose(_ws: WebSocket) {
    // No-op; runtime removes from getWebSockets() when closed
  }

  async webSocketError(_ws: WebSocket) {
    // No-op; runtime removes from getWebSockets() when closed
  }
}