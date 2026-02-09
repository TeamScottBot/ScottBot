import { IoPerson } from "react-icons/io5";
import { PiArrowBendDownRightThin } from "react-icons/pi";


const CustomerDashboard = () => {
  return (
    <div className="flex flex-col mt-36 text-black font-semibold">
      <div className="flex flex-col items-center">
        <div className="flex bg-scott-grey-200 w-40 h-40 items-center justify-center rounded-full">
            <IoPerson className="text-8xl text-scott-grey-100"/>
        </div>
          <div className="text-4xl text-center mt-4">
            Hi, Cade
        </div>
      </div>
      <div className="items-start mt-8 text-xl">
        <div className="">
          Looks like you're located at:
        </div>
        <div className="underline">
          Winston Chung
        </div>
      </div>
      <div className="flex row justify-end mt-0 text-lg font-medium">
        <PiArrowBendDownRightThin className="text-6xl font-light mr-24" />
        <div className="text-right">
          Let's take a look at <br /> your options
        </div>
      </div>
    </div>
  );
};

export default CustomerDashboard;