import { z } from "zod"

export const OrderSchema = z.object({
  status: z.enum(["test", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff", "delivered"]).default("test")
})

export type OrderState = {
  id: string
  status: string
}