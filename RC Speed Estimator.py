import math
import tkinter as tk
appWindow = tk.Tk()
greeting = tk.Label(text="Radio Controlled Car Speed Estimator")
greeting.pack()




motorKV = int(input("Motor kV rating: "))
battVolt = float(input("Battery Voltage: "))
pinion = int(input("Pinion teeth count: "))
spur = int(input("Spur teeth count: "))
finalGearRatio = float(input("Final Gear Ratio (differentials?): "))
wheelCircum = (2*math.pi)*float(input("Wheel radius in inches: "))
totalRPM = motorKV * battVolt

speed = (totalRPM / ((spur/pinion) * finalGearRatio)) * (wheelCircum / 12) * 60 / 5280


print("Final estimated speed in mph: ", speed)

