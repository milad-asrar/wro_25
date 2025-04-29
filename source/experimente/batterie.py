from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor,ColorSensor,UltrasonicSensor
from pybricks.parameters import Button,Color,Direction,Port,Side,Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait,StopWatch
 
hub=PrimeHub()
def get_battary_status():
    voltage=hub.battery.voltage()
    battery=0
    VMAX=8300
    VMIN=6000
    if voltage>=VMAX:
        print("battery is at 100%")
    elif voltage<=VMIN:
        print("battery is at 1% or less")
    else:
        battery=(voltage-VMIN)*100/(VMAX-VMIN)
        print(f"battery is at {round(battery)}%, volts={voltage}")
    return round(battery)
battery_prozent = get_battary_status()
print(battery_prozent)