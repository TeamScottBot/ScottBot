import { z } from "zod"

export const OrderSchema = z.object({
  pickupLocation: z.string(),
  dropoffLocation: z.string(),
  status: z.enum(["test", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff", "delivered"]).default("test")
})

export type OrderState = {
  id: string
  pickupLocation: string
  dropoffLocation: string
  status: string
}