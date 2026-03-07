"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ROBOT_ID, initRobot, startOrder } from "@/lib/api";

const CUSTOMER_LOCATION = "Winston Chung";

const RestarauntSelect = () => {
  const router = useRouter();
  const [selected, setSelected] = useState<string | null>(null);
  const [placing, setPlacing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handlePlaceOrder = async () => {
    const pickup = selected ?? "Panda Express";
    setError(null);
    setPlacing(true);
    try {
      await initRobot();
      const { orderId } = await startOrder(ROBOT_ID, {
        pickupLocation: pickup,
        dropoffLocation: CUSTOMER_LOCATION,
      });
      if (typeof window !== "undefined") sessionStorage.setItem("orderId", orderId);
      router.push("/activeOrder");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to place order");
    } finally {
      setPlacing(false);
    }
  };

  const restos = [
    { name: "Panda Express", value: "Panda Express" },
    { name: "Subway", value: "Subway" },
    { name: "Habit Burger", value: "Habit Burger" },
  ];

  return (
    <div className="flex flex-col mt-12 text-black font-semibold">
      <div className="flex flex-col items-center">
        <div className="flex flex-col bg-scott-grey-200 w-23/24 items-center justify-center rounded-2xl">
          {restos.map((r, i) => (
            <button
              key={r.value}
              type="button"
              className={`flex w-11/12 h-18 items-center justify-center rounded-2xl text-semibold text-lg border-2 border-transparent ${i === 0 ? "mt-4" : i === restos.length - 1 ? "my-4" : "mt-4"} ${
                selected === r.value
                  ? "bg-scott-grey-100 text-white"
                  : "bg-white text-black hover:bg-scott-grey-100 hover:text-white"
              }`}
              onClick={() => setSelected(r.value)}
            >
              {r.name}
            </button>
          ))}
        </div>
        {error && (
          <p className="mt-2 text-sm text-red-600 w-23/24 text-center font-medium" role="alert">
            {error}
          </p>
        )}
        <button
          type="button"
          className="flex bg-black w-23/24 h-18 mt-8 mb-12 items-center justify-center rounded-2xl text-white text-semibold text-2xl hover:bg-scott-grey-300 hover:text-black disabled:opacity-70 mx-auto"
          onClick={handlePlaceOrder}
          disabled={placing}
        >
          {placing ? "Placing…" : "Place Order"}
        </button>
      </div>
    </div>
  );
};

export default RestarauntSelect;