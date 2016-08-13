import RPi.GPIO as GPIO
from input import *

pin_left = 24
pin_right = 23
pin_enter = 22
pin_back = 27

GPIO.setmode(GPIO.BCM)

for pin in [pin_left, pin_right, pin_enter, pin_back]:
	GPIO.setup(pin, GPIO.IN)

def switch(key):
	if key_state[key]:
		release(key)
	else: press(key)

def check():
	if GPIO.input(pin_left) == key_state[Key.LEFT]:
		switch(Key.LEFT)
	if GPIO.input(pin_right) == key_state[Key.RIGHT]:
		switch(Key.RIGHT)
	if GPIO.input(pin_enter) == key_state[Key.ENTER]:
		switch(Key.ENTER)
	if GPIO.input(pin_back) == key_state[Key.BACK]:
		switch(Key.BACK)

on_tick.append(check)
available_input_methods.append("buttons")
