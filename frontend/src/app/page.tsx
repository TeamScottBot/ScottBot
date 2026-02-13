import CustomerDashboard from "@/components/customer/customerDashboard";
import RestarauntSelect from "@/components/customer/restarauntSelect";

const Home = () => {
	return (
		<div className="bg-white text-black mx-auto">
			<CustomerDashboard />
			<RestarauntSelect />
		</div>
	);
};
export default Home;
