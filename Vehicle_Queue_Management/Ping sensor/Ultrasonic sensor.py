import time
import RPi.GPIO as G

# Use BCM GPIO references
# instead of physical pin numbers
G.setmode(G.BOARD)
G.setwarnings(False)

# Define GPIO to use on Pi
GPIO_TRIGGER = 11
GPIO_ECHO    = 13



# Set pins as output and input
G.setup(GPIO_TRIGGER,G.OUT)  # Trigger
G.setup(GPIO_ECHO,G.IN)      # Echo


while True:
    
    G.output(GPIO_TRIGGER, False)

    print "Ultrasonic Measurement"

    # Allow module to settle
    time.sleep(0.5)

    # Send 10us pulse to trigger
    G.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    G.output(GPIO_TRIGGER, False)
    start = time.time()

    while G.input(GPIO_ECHO)==0:
        start = time.time()

    while G.input(GPIO_ECHO)==1:
        stop = time.time()
 
    # Calculate pulse length
    elapsed = stop-start

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distancet = elapsed * 34300

   # That was the distance there and back so halve the value
    distance = distancet / 2

    if distance > 2 and distance < 100:      #Check whether the distance is within range
        print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
        time.sleep(2)
    else:
        print "Out Of Range"                   #display out of range
        time.sleep(2)



# Reset GPIO settings
G.cleanup()

# Set trigger to False (Low)
