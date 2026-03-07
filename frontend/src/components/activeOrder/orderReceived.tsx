"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ROBOT_ID, getOrderStatus, deleteOrder } from "../../lib/api";

const OrderReceived = () => {
  const queryClient = useQueryClient();
  const { data } = useQuery({
    queryKey: ["orderStatus", ROBOT_ID],
    queryFn: () => getOrderStatus(ROBOT_ID),
    refetchInterval: 5000,
  });

  const clearOrderMutation = useMutation({
    mutationFn: () => deleteOrder(ROBOT_ID),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orderStatus", ROBOT_ID] });
    },
  });

  const status = data && "status" in data ? data.status : "idle";
  const isDelivered = status === "delivered";
  const hasActiveOrder = data && "id" in data && status !== "idle";

  return (
    <div className="flex flex-col mt-12 text-black font-semibold">
      <div className="flex flex-col items-center">
        <button
          type="button"
          className="flex bg-black w-23/24 h-18 mt-8 mb-12 items-center justify-center rounded-2xl text-white text-semibold text-2xl hover:bg-scott-grey-300 hover:text-black disabled:opacity-70 mx-auto"
          onClick={() => clearOrderMutation.mutate()}
          disabled={!isDelivered || clearOrderMutation.isPending}
        >
          {clearOrderMutation.isPending
            ? "Clearing…"
            : "Order Received!"}
        </button>
        {hasActiveOrder && !isDelivered && (
          <p className="text-scott-grey-300 text-sm -mt-8 mb-4">
            Available when order is delivered
          </p>
        )}
      </div>
    </div>
  );
};

export default OrderReceived;