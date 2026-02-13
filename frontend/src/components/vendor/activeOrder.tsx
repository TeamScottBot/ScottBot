const ActiveOrder = () => {
  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 rounded-2xl">
            <div className="mt-4 ml-4 text-left text-lg">
                Active Order
            </div>
            <div className="flex bg-white w-11/12 h-18 my-4 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Cade
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Panda Express
                </div>
            </div>
            <button className="flex bg-black w-11/12 h-18 mb-4 items-center justify-center rounded-2xl text-white font-semibold text-xl hover:bg-scott-grey-300 hover:text-black mx-auto">
                Deliver Order
            </button>
            </div>
        </div>
    </div>

  );
};


export default ActiveOrder;