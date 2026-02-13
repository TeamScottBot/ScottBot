
import { Hono } from "hono"
import { zValidator } from "@hono/zod-validator"
import { OrderSchema } from "../types"

type Env = {
  ORDERS: DurableObjectNamespace
}

export const ordersRoutes = new Hono<{ Bindings: Env }>()

ordersRoutes.post(
  "/",
  zValidator("json", OrderSchema),
  async (c) => {
    const body = c.req.valid("json")
    const id = crypto.randomUUID()

    const stub = c.env.ORDERS.get(
      c.env.ORDERS.idFromName(id)
    )

    await stub.fetch("https://do/init", {
      method: "POST",
      body: JSON.stringify({
        id,
        status: body.status ?? "test"
      })
    })

    return c.json({ orderId: id })
  }
)

ordersRoutes.get("/:id/status", async (c) => {
  const id = c.req.param("id")

  const stub = c.env.ORDERS.get(
    c.env.ORDERS.idFromName(id)
  )

  const res = await stub.fetch("https://do/status", {
    method: "GET"
  })

  if (!res.ok) {
    return c.json({ error: "Order not found" }, 404)
  }

  return res
})

ordersRoutes.post(
  "/:id/update",
  zValidator("json", OrderSchema),
  async (c) => {
    const id = c.req.param("id")
    const body = c.req.valid("json")
    const status = body.status

    const stub = c.env.ORDERS.get(
      c.env.ORDERS.idFromName(id)
    )

    const res = await stub.fetch("https://do/update", {
      method: "POST",
      body: JSON.stringify({ status })
    })

    if (!res.ok) {
      return c.json({ error: "Order not found" }, 404)
    }

    return res
  }
)

ordersRoutes.delete("/:id", async (c) => {
  const id = c.req.param("id")

  const stub = c.env.ORDERS.get(
    c.env.ORDERS.idFromName(id)
  )

  const res = await stub.fetch("https://do/delete", {
    method: "DELETE"
  })

  if (!res.ok) {
    return c.json({ error: "Order not found" }, 404)
  }

  return c.json({ ok: true, orderId: id })
})