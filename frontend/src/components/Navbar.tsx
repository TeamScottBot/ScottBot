"use client";
import { usePathname } from "next/navigation";
import { IoPerson } from "react-icons/io5";
import { GiKnifeFork } from "react-icons/gi";
import { RiRobot2Line } from "react-icons/ri";
import Link from "next/link";

const items = [
  { name: "Customer", link: "/", icon: IoPerson },
  { name: "Vendor", link: "/vendor", icon: GiKnifeFork },
  { name: "Robot Control", link: "/robot", icon: RiRobot2Line },
];

const Navbar = () => {
  const pathname = usePathname();

  return (
    <div className="flex h-12 w-full bg-scott-grey-200 rounded-full items-center justify-center">
        <div className="flex flex-row gap-0 text-sm text-center font-semibold text-black">
          {items.map(({ link, name, icon: Icon }) => (
          <div key={link}>
            <Link
              href={link}
              className={`inline-flex items-center justify-between h-8 px-4 rounded-full transition-all duration-200 hover:scale-105 ${
                pathname === link
                  ? " bg-white"
                  : ""
              }`}
            >
              <Icon className="text-lg" />
              <span>{name}</span>
              </Link>
            </div>
          ))}
        </div>
    </div>
  );
};

export default Navbar;
