import Header from "@/components/robot/header";
import RouteRobot from "@/components/robot/routeRobot";
import RobotStatus from "@/components/robot/robotStatus";
import RobotControls from "@/components/robot/robotControls";


const Vendor = () => {
  return (
    <div className="bg-white text-black mx-auto">
        <Header />
        <RouteRobot/>
        <RobotStatus />
        <RobotControls />
    </div>
  )
};

export default Vendor;
