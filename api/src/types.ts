import { z } from "zod"

export const OrderSchema = z.object({
  pickupLocation: z.string(),
  dropoffLocation: z.string(),
  status: z.enum(["idle", "moving_to_pickup", "waiting_for_pickup", "moving_to_dropoff", "waiting_for_dropoff", "delivered"]).default("idle")
})

export type OrderState = {
  id: string
  pickupLocation: string
  dropoffLocation: string
  status: string
}