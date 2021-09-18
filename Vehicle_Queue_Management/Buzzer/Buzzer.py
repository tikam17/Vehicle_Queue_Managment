import RPi.GPIO as G
import time
G.setwarnings(False)
G.setmode(G.BOARD)
G.setup(11,G.IN)
G.setup(16,G.OUT)
while True:
	i=G.input(11)
	if i==0:
		print("No Obstacle")
		time.sleep(1)
	elif i==1:
		print("Obstacle detected")
		G.output(16,True)
		time.sleep(1)
		G.output(16,False)
