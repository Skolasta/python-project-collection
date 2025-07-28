import time
from playsound import playsound
import os 
alarm = "alarm.mp3"

try:
	minute = int(input("You must enter how many minutes you will work"))
	second = minute * 60
	print(f"Your {minute}-minute work session has started.")
	time.sleep(second)
	print("Time's up, you can take a break.")
	if os.path.exists(alarm):
		playsound(alarm) 
	else:
		print("Alarm not found")
		print(f"Please add a sound file named ‘{alarm}’ to the folder where the program is located.")
except Exception as e:
	print("Alarm did not work", e)
