import RPi.GPIO as gpio
import smbus

def highLow(prev, pinNum):
	curr = gpio.input(pinNum)
	if prev != curr:
		if curr == 0:
			print("GPIO pin " + str(pinNum) + " is LOW")
		else:
			print("GPIO pin " + str(pinNum) + " is High")
		return curr
	return prev

gpio.setmode(gpio.BCM)
# BLATS
gpio.setup(5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(13, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(19, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)



p1 = gpio.input(5)
p2 = gpio.input(6)
p3 = gpio.input(12)
p4 = gpio.input(13)
p5 = gpio.input(19)
p6 = gpio.input(26)

while True:	
	p1 = highLow(p1, 5)
	p2 = highLow(p2, 6)
	p3 = highLow(p3, 12)
	p4 = highLow(p4, 13)
	p5 = highLow(p5, 19)
	p6 = highLow(p6, 26)
