import { Hono } from "hono"
import { ordersRoutes } from "./routes/order"
import { OrderDO } from "./durable-objects/orders"

type Env = {
  ORDERS: DurableObjectNamespace
}

const app = new Hono<{ Bindings: Env }>()

app.route("/orders", ordersRoutes)

export default app
export { OrderDO }