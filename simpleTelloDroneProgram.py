from djitellopy import Tello
import cv2
import time


# ####NOTE####
# This isnt really the best way to control a tello, or any drone.
# This was one of my first programs i made using djitellopy.
# I'd recomend using "telloKeyboardControl.py" also in my repository.
# ############

#translates the command given in the input to useable commands by the drone, limmited and NOT GOOD.
def translateCommands(command):
    if command == "":
        return f"emergency()"
    elif command == "land":
        return f"land()"
    elif command == "takeoff":
        return f"takeoff()"
    try:
        main = command.split(" ")[0]
        num = command.split(" ")[1]
        if main == "clockwise":
            return f"rotate_clockwise({num})"
        elif main == "counterClockwise":
            return f"rotate_counter_clockwise({num})"
        elif main == "moveDown":
            return f"move_down({num})"
        elif main == "moveUp":
            return f"move_up({num})"
        elif main == "go":
            return f"send_rc_control(0, {num}, 0, 0)"
    except Exception:
        print(Exception)

WIDTH = 320
HEIGHT = 240
startCounter = 0 #0 is flight Mode 1 is testing 

#Connecting and Initilizations
drone = Tello()
drone.connect()
drone.for_back_velocity = 0
drone.left_right_velocity = 0
drone.up_down_velocity = 0
drone.yaw_velocity = 0
drone.speed = 0

batteryPercent = drone.get_battery()
print(batteryPercent)

#turn video stream off
drone.streamoff()
#turn it on
drone.streamon()

drone.send_rc_control(0, 0, 0, 0)
while True:
    #get the drone fottage
    frameRead = drone.get_frame_read()
    myFrame = frameRead.frame
    #resize the image to make it look somewhat good (still not good)
    img = cv2.resize(myFrame, (WIDTH, HEIGHT))

    #start counter checker
    if startCounter == 0:
        drone.takeoff()
        startCounter = 1

    #showing the drone footage
    cv2.imshow("Drone Footage", img)

    #enter a command for the drone to do this will block the footage since it is an input (VERY BAD)
    cmd = input("<CMD>: ")
    #very hacky way of doing it not recomended for use
    eval(f"drone.{translateCommands(cmd)}")

    #press q to quit the program, but first input command, since it stalls on that
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

#press enter to ACTIVATE EMERGENCY LANDING
land = input("ACTIVATE EMERGENCY LANDING: ")
drone.emergency()