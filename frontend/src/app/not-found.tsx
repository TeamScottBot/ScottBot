"use client";
import Link from "next/link";

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-black font-semibold">
      <div className="flex flex-col items-center w-11/12 bg-white rounded-2xl shadow-lg p-10">
        
        <div className="text-6xl mb-4">
          404
        </div>

        <div className="text-xl mb-6">
          Page Not Found
        </div>

        <Link
          href="/"
          className="flex bg-black w-48 h-14 items-center justify-center rounded-2xl text-white font-semibold text-lg hover:bg-scott-grey-300 hover:text-black transition duration-200"
        >
          Go Back Home
        </Link>

      </div>
    </div>
  );
};

export default NotFound;
