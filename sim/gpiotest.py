import RPi.GPIO as gpio
import smbus

gpio.setmode(gpio.BCM)
# BLATS
gpio.setup(5, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(6, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(13, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(19, gpio.IN, pull_up_down=gpio.PUD_DOWN)
gpio.setup(26, gpio.IN, pull_up_down=gpio.PUD_DOWN)



print(gpio.input(5))
print(gpio.input(6))
print(gpio.input(12))
print(gpio.input(13))
print(gpio.input(19))
print(gpio.input(26))

