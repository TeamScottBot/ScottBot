import { Hono } from "hono"
import { cors } from "hono/cors"
import { ordersRoutes } from "./routes/order"
import { OrderDO } from "./durable-objects/orders"

type Env = {
  ORDERS: DurableObjectNamespace
}

const app = new Hono<{ Bindings: Env }>()

app.use("*", cors())

app.route("/orders", ordersRoutes)

export default app
export { OrderDO }