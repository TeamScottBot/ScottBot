const RouteRobot = () => {
  return (
    <div className="flex flex-col mt-8 text-black font-semibold">
      <div className="flex flex-col items-center">
        <div className="flex flex-col bg-scott-grey-200 w-11/12 rounded-2xl p-4">
          
          <label className="text-lg mb-2" htmlFor="route">
            Route to Location
          </label>
          <select
            id="route"
            className="w-full bg-white h-12 rounded-2xl px-4 mb-4 text-scott-grey-100 text-sm focus:outline-none focus:ring-2 focus:ring-black"
          >
            <option value="panda-express">Panda Express</option>
            <option value="subway">Subway</option>
            <option value="habit-burger">Habit Burger</option>
            <option value="coffee-bean">Coffee Bean</option>
            <option value="bytes">Bytes</option>
            <option value="hibachi-san">Hibachi San</option>
          </select>

          <button className="flex bg-black w-full h-16 mb-2 items-center justify-center rounded-2xl text-white font-semibold text-xl hover:bg-scott-grey-300 hover:text-black">
            Start
          </button>
        </div>
      </div>
    </div>
  );
};

export default RouteRobot;
