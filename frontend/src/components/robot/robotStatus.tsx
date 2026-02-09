const RobotStatus = () => {
  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 rounded-2xl">
            <div className="mt-4 ml-4 text-left text-lg">
                Robot Status
            </div>
            <div className="flex bg-white w-11/12 h-18 my-4 items-center justify-between rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                Order in Progress
                </div>
                <div className="text-scott-grey-300 text-right mr-4">
                Delivering to: <br />Winston Chung
                </div>
            </div>
            </div>
        </div>
    </div>

  );
};


export default RobotStatus;