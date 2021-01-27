import time
import RPi.GPIO as GPIO
import random
from pygame import mixer

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

# GPIO-pins used for lights (4 is green, so it goes all red -> green -> back n forth all green)
pins = [5, 25, 22, 27, 17, 4, 17, 27, 22, 25, 5, 6]

# GPIO-pins without the green one, used so they can blink
pins_uten_gronn = [17, 27, 22, 25, 5, 6]

# Sets up all pins

for x in pins:
	GPIO.setup(x, GPIO.OUT)

GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonPress = True

# This is what runs when the game is activated

def BlinkGame():
	# Random start time between 3 and 5 mins and end time is current time + number of seconds
	sek = random.randint(180, 300)
	t_end = time.time() + sek
	print(sek)
	# While loop runs while current time is lower than end time
	while time.time() < t_end:
		for x in pins:
			#Will go back and forth with the lights and play ticking sound while looking for button press
			GPIO.output(x, True)
			time.sleep(.25)
			buttonPress = GPIO.input(26)
			GPIO.output(x, False)
			mixer.init()
			mixer.music.load('/home/pi/prosjekt/Tick.mp3')
			mixer.music.play()
			if buttonPress == False:
				# If button press at green light, play ding and flash green light 10 times
				if x == 4:
					h = 0
					mixer.init()
					mixer.music.load('/home/pi/prosjekt/Ding.mp3')
					mixer.music.play()
					while h < 10:
						GPIO.output(4, True)
						time.sleep(.1)
						GPIO.output(4, False)
						time.sleep(.1)
						h += 1
				# If button press at red light, play bruh and flash red lights 10 times
				else:
					h = 0
					t_end -= 15
					mixer.init()
					mixer.music.load('/home/pi/prosjekt/Bruh.mp3')
					mixer.music.play()
					while h < 10:
						for i in pins_uten_gronn:
							GPIO.output(i, True)
						time.sleep(.1)
						for i in pins_uten_gronn:
							GPIO.output(i, False)
						time.sleep(.1)
						h += 1
	mixer.init()
	mixer.music.load('/home/pi/prosjekt/Boom.mp3')
	mixer.music.play()
	time.sleep(15)

#This is the code that runs in idle-mode, will activate game at button press

try:
	while True:
		for x in pins:
			buttonPress = GPIO.input(26)
			if buttonPress == False:
				BlinkGame()
			GPIO.output(x, True)
			time.sleep(1)
			GPIO.output(x, False)
finally:
	GPIO.cleanup()