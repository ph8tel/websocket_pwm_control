import asyncio
import websockets
import json
from PCA9685 import PCA9685
from time import ctime
import threading
from campower import CamPower
print("start")
cams = CamPower(21, 20, 16, 12)
# what kind of PWM dedicated chip wou are using
pwm = PCA9685(0x40)
# cylce frequency of that chip
pwm.setPWMFreq(50)
# Pos is the exact servo position
# start the servos in the middle
Pos0 = 1500
Pos1 = 1500
Pos2 = 1500
Pos3 = 1500
# Steps are how much to move, not the movement (Pos)
Steps = [0, 0, 0, 0, 0, 0, 0]
# start the servos in the middle
pwm.setServoPulse(0, Pos0)
pwm.setServoPulse(1, Pos1)
pwm.setServoPulse(2, Pos2)
pwm.setServoPulse(3, Pos3)

# this will be threaded to a dedicated core and run every .02 seconds
def timerfunc():
    global Steps, Pos0, Pos1, Pos2, Pos3, pwm
    # Check for new steps and then move within servo limits
    if (Steps[0] != 0):
        Pos0 += Steps[0]
        if (Pos0 >= 2500):
            Pos0 = 2500
        if (Pos0 <= 500):
            Pos0 = 500
        print('setting 0', Pos0)  # set channel 0
        pwm.setServoPulse(0, Pos0)

    if (Steps[1] != 0):
        Pos1 += Steps[1]
        if (Pos1 >= 2500):
            Pos1 = 2500
        if (Pos1 <= 500):
            Pos1 = 500
        # set channel 1
        print('setting 1', Pos1)
        pwm.setServoPulse(1, Pos1)

    if (Steps[2] != 0):
        Pos2 += Steps[2]
        if (Pos2 >= 2500):
            Pos2 = 2500
        if (Pos2 <= 500):
            Pos2 = 500
        # set channel 2
        print('setting 2', Pos2)
        pwm.setServoPulse(2, Pos2)

    if (Steps[3] != 0):
        Pos3 += Steps[3]
        if (Pos3 >= 2500):
            Pos3 = 2500
        if (Pos3 <= 500):
            Pos3 = 500
        # set channel 3
        print('setting 3', Pos3)
        pwm.setServoPulse(3, Pos3)


# This handles a GPIO controlled H-Bridge modified to be a 12V 1 in 4 out selective power relay
# You should filter the 5v if you're planning on tapping it to run the Pi (add a capacitor too because servos can be high load)
def setSwitches(commands):
    #which camera to control
    cameraIndex = commands[1]
    #on (1) or off (0)
    cameraCommand = commands[2]
    print(f"camera: {cameraIndex}, cameraCommand: {'on' if cameraCommand == 1 else 'off'}")
    if cameraIndex == 0:
        if cameraCommand == 1:
            cams.all_on()
        if cameraCommand == 0:
            cams.all_off()
    if cameraIndex == 1:
        if cameraCommand == 1:
            cams.cam_a_on()
        if cameraCommand == 0:
            cams.cam_a_off()
    if cameraIndex == 2:
        if cameraCommand == 1:
            cams.cam_b_on()
        if cameraCommand == 0:
            cams.cam_b_off()
    if cameraIndex == 3:
        if cameraCommand == 1:
            cams.cam_c_on()
        if cameraCommand == 0:
            cams.cam_c_off()
    if cameraIndex == 4:
        if cameraCommand == 1:
            cams.cam_d_on()
        if cameraCommand == 0:
            cams.cam_d_off()

async def routeCommands(websocket, path):
    while True:
        commands = None
        incomingMessageJSON = await websocket.recv()
        try:
            commands = json.loads(incomingMessageJSON)
        except:
            commands = [99]
        finally:
            if commands[0] == 90:
                setSwitches(commands)
            elif commands[0] == 80 or commands[0] == 70:
                Steps = commands[1:-1]
            elif commands[0] == 99:
                print('New Client: ', commands)

            await websocket.send("ok")


start_server = websockets.serve(routeCommands, "0.0.0.0", 8888)
# dedicate core to thread
t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()
# start socket server process loop
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
