const OrderReceived = () => {
  return (
    <div className="flex flex-col mt-12 text-black font-semibold">
      <div className="flex flex-col items-center">
        <button className="flex bg-black w-23/24 h-18 mt-8 mb-12 items-center justify-center rounded-2xl text-white text-semibold text-2xl hover:bg-scott-grey-300 hover:text-black">
            Order Received!
        </button>
      </div>
    </div>
  );
};

export default OrderReceived;