import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ReactQueryClientProvider } from "@/utils/react-query";
import Navbar from "@/components/Navbar";
import "./globals.css";

const inter = Inter({
	variable: "--font-geist-sans",
	subsets: ["latin"],
});

export const metadata: Metadata = {
	title: "ScottBot",
	description: "UCR 179M AI Project",
};

export default function RootLayout({
	children,
}: Readonly<{
	children: React.ReactNode;
}>) {
	return (
		<html lang="en">
			<body className={inter.className}>
				<ReactQueryClientProvider>
				<header className="w-full border-b">
					<div className="mx-auto max-w-[436px] px-6">
						<Navbar />
					</div>
				</header>

				<main className="mx-auto w-full max-w-[436px] px-6">
					{children}
				</main>
				</ReactQueryClientProvider>
			</body>
		</html>
	);
}
