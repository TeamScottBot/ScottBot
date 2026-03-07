"use client";

import { useQuery } from "@tanstack/react-query";
import { ROBOT_ID, getOrderStatus, getOrderWebSocketUrl } from "@/lib/api";
import { useEffect, useState } from "react";

const statusLabel: Record<string, string> = {
  idle: "Idle",
  moving_to_pickup: "Order in Progress",
  waiting_for_pickup: "Order in Progress",
  moving_to_dropoff: "Order in Progress",
  waiting_for_dropoff: "Order in Progress",
  delivered: "Delivered",
};

const OrderStatus = () => {
  const [wsStatus, setWsStatus] = useState<{ status: string; dropoffLocation?: string } | null>(null);

  const { data, refetch } = useQuery({
    queryKey: ["orderStatus", ROBOT_ID],
    queryFn: () => getOrderStatus(ROBOT_ID),
    refetchInterval: 5000,
  });

  useEffect(() => {
    const url = getOrderWebSocketUrl(ROBOT_ID);
    const ws = new WebSocket(url);
    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data as string);
        if (msg.type === "connected") return;
        setWsStatus({
          status: msg.status,
          dropoffLocation: msg.dropoffLocation,
        });
      } catch {
        // ignore
      }
    };
    return () => ws.close();
  }, []);

  const display = wsStatus ?? data;
  const status = display && "status" in display ? display.status : "idle";
  const dropoff =
    display && "dropoffLocation" in display && display.dropoffLocation
      ? display.dropoffLocation
      : "Winston Chung";
  const label = statusLabel[status] ?? "Order in Progress";

  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 rounded-2xl">
            <div className="mt-4 ml-4 text-left text-lg">
                Active Order
            </div>
            <div className="flex bg-white w-11/12 h-18 my-4 items-center justify-between rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                {label}
                </div>
                <div className="text-scott-grey-300 text-right mr-4">
                Delivering to: <br />{dropoff}
                </div>
            </div>
            </div>
        </div>
    </div>
  );
};

export default OrderStatus;