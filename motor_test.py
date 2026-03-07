from REVHubInterface.REVcomm import REVcomm
import time

comm = REVcomm()
comm.openActivePort()

modules = comm.discovery()
module = modules[0]
print(f"Hub address: {module.getAddress()}")

for i in range(4):
    module.motors[i].setMode(0, 1)
    module.motors[i].enable()
    module.motors[i].setPower(6400)
    print(f"Motor {i} started!")

# Keep alive for 2 seconds
print("Running all motors for 2 seconds...")
start = time.time()
while time.time() - start < 2:
    module.sendKA()
    time.sleep(0.25)

# Stop all motors
for i in range(4):
    module.motors[i].setPower(0)
    module.motors[i].disable()
    print(f"Motor {i} stopped!")

comm.closeActivePort()
print("Done.")