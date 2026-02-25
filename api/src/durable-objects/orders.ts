import { OrderState } from "../types"

export class OrderDO {
  state: DurableObjectState
  clients: Set<WebSocket> = new Set()

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(req: Request) {
    const url = new URL(req.url)
    if (url.pathname === "/ws") {
      const pair = new WebSocketPair()
      const client = pair[1]

      this.state.acceptWebSocket(client)
      this.clients.add(client)

      return new Response(null, {
        status: 101,
        webSocket: pair[0]
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

    if (url.pathname === "/delete") {
      await this.state.storage.deleteAll()
      return Response.json({ deleted: true })
    }

    return new Response("not found", { status: 404 })
  }

  private broadcastToClients(data: unknown) {
    const message = JSON.stringify(data)
    const deadClients = []

    for (const client of this.clients) {
      try {
        client.send(message)
      } catch (error) {
        deadClients.push(client)
      }
    }

    for (const client of deadClients) {
      this.clients.delete(client)
    }
  }

  async webSocketMessage(ws: WebSocket, message: ArrayBuffer | string) {
    // Echo messages back if needed, or handle them here
  }

  async webSocketClose(ws: WebSocket) {
    this.clients.delete(ws)
  }

  async webSocketError(ws: WebSocket) {
    this.clients.delete(ws)
  }
}