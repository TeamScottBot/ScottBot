from REVHubInterface.REVcomm import REVcomm
import time

comm = REVcomm()
comm.openActivePort()

modules = comm.discovery()
module = modules[0]
print(f"Hub address: {module.getAddress()}")

def forward():
    for i in range(2):
        module.motors[i].setMode(0, 1)
        module.motors[i].enable()
        module.motors[i].setPower(9600)

    for i in range(2, 4):
        module.motors[i].setMode(0, 1)
        module.motors[i].enable()
        module.motors[i].setPower(-9600)
        print(f"Motor {i} started!")

def backward():
    for i in range(2):
        module.motors[i].setMode(0, 1)
        module.motors[i].enable()
        module.motors[i].setPower(-9600)

    for i in range(2, 4):
        module.motors[i].setMode(0, 1)
        module.motors[i].enable()
        module.motors[i].setPower(9600)
        print(f"Motor {i} started!")

def diagonalRightForward():
    module.motors[1].setMode(0, 1)
    module.motors[1].enable()
    module.motors[1].setPower(9600)

    module.motors[3].setMode(0, 1)
    module.motors[3].enable()
    module.motors[3].setPower(-9600)

def diagonalLeftForward():
    module.motors[0].setMode(0, 1)
    module.motors[0].enable()
    module.motors[0].setPower(9600)

    module.motors[2].setMode(0, 1)
    module.motors[2].enable()
    module.motors[2].setPower(-9600)

def right():
    module.motors[0].setMode(0, 1)
    module.motors[0].enable()
    module.motors[0].setPower(9600)

    module.motors[2].setMode(0, 1)
    module.motors[2].enable()
    module.motors[2].setPower(9600)

    module.motors[1].setMode(0, 1)
    module.motors[1].enable()
    module.motors[1].setPower(-9600)

    module.motors[3].setMode(0, 1)
    module.motors[3].enable()
    module.motors[3].setPower(-9600)

def left():
    module.motors[0].setMode(0, 1)
    module.motors[0].enable()
    module.motors[0].setPower(-9600)

    module.motors[2].setMode(0, 1)
    module.motors[2].enable()
    module.motors[2].setPower(-9600)

    module.motors[1].setMode(0, 1)
    module.motors[1].enable()
    module.motors[1].setPower(9600)

    module.motors[3].setMode(0, 1)
    module.motors[3].enable()
    module.motors[3].setPower(9600)

forward()
# Keep alive for 2 seconds
print("Running all motors for 2 seconds...")
start = time.time()
while time.time() - start < 5:
    module.sendKA()
    time.sleep(0.25)

# Stop all motors
for i in range(4):
    module.motors[i].setPower(0)
    module.motors[i].disable()
    print(f"Motor {i} stopped!")

comm.closeActivePort()
print("Done.")
