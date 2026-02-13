const RobotControls = () => {
  return (
    <div className="flex flex-col my-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 rounded-2xl">
            <div className="my-4 ml-4 text-left text-lg">
                Emergency Controls
            </div>
            <button className="flex bg-scott-red-100 w-11/12 h-18 mb-4 items-center justify-center rounded-2xl text-white font-semibold text-xl hover:text-black mx-auto">
                EMERGENCY STOP
            </button>
            </div>
        </div>
    </div>

  );
};


export default RobotControls;