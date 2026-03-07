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

  const handlePlaceOrder = async (e: React.MouseEvent) => {
    e.preventDefault();
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

  return (
    <div className="flex flex-col mt-12 text-black font-semibold">
      <div className="flex flex-col items-center">
        <div className="flex flex-col bg-scott-grey-200 w-23/24 items-center justify-center rounded-2xl">
           <button
             type="button"
             className="flex bg-white w-11/12 h-18 mt-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white"
             onClick={() => setSelected("Panda Express")}
           >
                Panda Express
            </button>
            <button
              type="button"
              className="flex bg-white w-11/12 h-18 mt-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white"
              onClick={() => setSelected("Subway")}
            >
                Subway
            </button>
            <button
              type="button"
              className="flex bg-white w-11/12 h-18 my-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white"
              onClick={() => setSelected("Habit Burger")}
            >
                Habit Burger
            </button>
        </div>
        {error && (
          <p className="mt-2 text-sm text-red-600 w-23/24 text-center">{error}</p>
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