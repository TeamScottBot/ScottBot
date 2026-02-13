import { OrderState } from "../types"

export class OrderDO {
  state: DurableObjectState

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(req: Request) {
    const url = new URL(req.url)

    if (url.pathname === "/init") {
      const { id, status } = await req.json<OrderState>()
      await this.state.storage.put("order", { id, status })
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
      await this.state.storage.put("order", { ...order, status })
      return Response.json({ ...order, status })
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
}