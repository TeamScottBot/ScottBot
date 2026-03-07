"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { ROBOT_ID, getOrderStatus, updateOrderStatus } from "@/lib/api";

const VendorActiveOrder = () => {
  const queryClient = useQueryClient();
  const { data } = useQuery({
    queryKey: ["orderStatus", ROBOT_ID],
    queryFn: () => getOrderStatus(ROBOT_ID),
    refetchInterval: 5000,
  });

  const deliverMutation = useMutation({
    mutationFn: (order: { pickupLocation: string; dropoffLocation: string }) =>
      updateOrderStatus(ROBOT_ID, { status: "delivered", ...order }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["orderStatus", ROBOT_ID] }),
  });

  const hasOrder = data && "id" in data && data.status !== "idle";
  const customer = hasOrder && "dropoffLocation" in data ? data.dropoffLocation : "Cade";
  const restaurant = hasOrder && "pickupLocation" in data ? data.pickupLocation : "Panda Express";

  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 rounded-2xl">
            <div className="mt-4 ml-4 text-left text-lg">
                Active Order
            </div>
            <div className="flex bg-white w-11/12 h-18 my-4 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    {customer}
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    {restaurant}
                </div>
            </div>
            <button
              type="button"
              className="flex bg-black w-11/12 h-18 mb-4 items-center justify-center rounded-2xl text-white font-semibold text-xl hover:bg-scott-grey-300 hover:text-black mx-auto disabled:opacity-70"
              onClick={() =>
                hasOrder &&
                "pickupLocation" in data &&
                "dropoffLocation" in data &&
                deliverMutation.mutate({
                  pickupLocation: data.pickupLocation,
                  dropoffLocation: data.dropoffLocation,
                })
              }
              disabled={!hasOrder || deliverMutation.isPending}
            >
                {deliverMutation.isPending ? "Updating…" : "Deliver Order"}
            </button>
            </div>
        </div>
    </div>
  );
};

export default VendorActiveOrder;