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
      const { id, pickupLocation, dropoffLocation, status } = await req.json<OrderState>()
      await this.state.storage.put("order", { id, pickupLocation, dropoffLocation, status })
      const orderData = {
        orderId: id,
        pickupLocation,
        dropoffLocation,
        status
      }
      this.broadcastToClients(orderData)

      return new Response("ok")
    }

    if (url.pathname === "/status") {
      const order = await this.state.storage.get<OrderState>("order")
      if (!order) {
        return new Response("not found", { status: 404 })
      }
      return Response.json(order)
    }

    if (url.pathname === "/update") {
      const { status } = await req.json<{ status: string }>()
      const order = await this.state.storage.get<OrderState>("order")

      if (!order) {
        return new Response("not found", { status: 404 })
      }
      const updatedOrder = { ...order, status }
      await this.state.storage.put("order", updatedOrder)

      this.broadcastToClients({
        orderId: order.id,
        pickupLocation: order.pickupLocation,
        dropoffLocation: order.dropoffLocation,
        status
      })

      return Response.json(updatedOrder)
    }

    if (url.pathname === "/delete") {
      const order = await this.state.storage.get<OrderState>("order")
      if (!order) {
        return new Response("not found", { status: 404 })
      }
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

  // async webSocketMessage(ws: WebSocket, message: ArrayBuffer | string) {
  // }

  async webSocketClose(ws: WebSocket) {
    this.clients.delete(ws)
  }

  async webSocketError(ws: WebSocket) {
    this.clients.delete(ws)
  }
}