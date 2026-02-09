const ActiveOrder = () => {
  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
        <div className="flex flex-col items-center">
            <div className="flex flex-col bg-scott-grey-200 w-23/24 mb-12 rounded-2xl">
            <div className="my-4 ml-4 text-left text-lg">
                Upcoming Orders
            </div>
            <div className="flex bg-white w-11/12 h-18 my-2 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Cade
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Subway
                </div>
            </div>
            <div className="flex bg-white w-11/12 h-18 my-2 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Cole
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Halal Shack
                </div>
            </div>
            <div className="flex bg-white w-11/12 h-18 my-2 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Quin
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Chronic Tacos
                </div>
            </div>
            <div className="flex bg-white w-11/12 h-18 my-2 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Risa
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Bytes
                </div>
            </div>
            <div className="flex bg-white w-11/12 h-18 mt-2 mb-4 items-center justify-start rounded-2xl text-black text-sm mx-auto">
                <div className="text-black ml-4">
                    Nolan
                </div>
                <div className="text-scott-grey-300 text-right ml-2">
                    Panda Express
                </div>
            </div>
            </div>
        </div>
    </div>

  );
};


export default ActiveOrder;