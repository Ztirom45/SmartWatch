
all:
	ampy --port /dev/ttyACM0 run src/main.py

ls:
	ampy --port /dev/ttyACM0 ls
