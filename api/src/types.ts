import { z } from "zod"

export const CreateOrderSchema = z.object({
  status: z.string().default("test")
})

export type OrderState = {
  id: string
  status: string
}