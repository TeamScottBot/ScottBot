const CustomerDashboard = () => {
  return (
    <div className="flex flex-col mt-12 text-black font-semibold">
      <div className="flex flex-col items-center">
        <div className="flex flex-col bg-scott-grey-200 w-23/24 items-center justify-center rounded-2xl">
           <button className="flex bg-white w-11/12 h-18 mt-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white">
                Panda Express
            </button>
            <button className="flex bg-white w-11/12 h-18 mt-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white">
                Subway
            </button>
            <button className="flex bg-white w-11/12 h-18 my-4 items-center justify-center rounded-2xl text-black text-semibold text-lg hover:bg-scott-grey-100 hover:text-white">
                Habit Burger
            </button>
        </div>
        <button className="flex bg-black w-23/24 h-18 mt-8 mb-12 items-center justify-center rounded-2xl text-white text-semibold text-2xl hover:bg-scott-grey-300 hover:text-black">
            Place Order
        </button>
      </div>
    </div>
  );
};

export default CustomerDashboard;