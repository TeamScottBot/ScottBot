import Header from "@/components/vendor/header";
import RobotStatus from "@/components/robot/robotStatus";
import ActiveOrder from "@/components/vendor/activeOrder";
import UpcomingOrders from "@/components/vendor/upcomingOrders";

const Vendor = () => {
  return (
    <div className="bg-white text-black mx-auto">
        <Header />
        <RobotStatus />
        <ActiveOrder />
        <UpcomingOrders />
    </div>
  )
};

export default Vendor;
