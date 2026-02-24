import Header from "@/components/activeOrder/header";
import OrderStatus from "@/components/activeOrder/orderStatus";
import OrderReceived from "@/components/activeOrder/orderReceived";

const ActiveOrder = () => {
  return (
    <div className="bg-white text-black mx-auto">
        <Header />
        <OrderStatus />
        <OrderReceived />
    </div>
  )
};

export default ActiveOrder;
