import RPi.GPIO as G
import time
from subprocess import call
from RPLCD.gpio import CharLCD
import paho.mqtt.client  as  mqtt

G.setwarnings(False)
G.setmode(G.BOARD)
G.setup(16,G.OUT) # for buzzer
G.setup(12,G.OUT) # for opening gate
GPIO_TRIGGER = 11
GPIO_ECHO    = 13
G.setup(GPIO_TRIGGER,G.OUT)  # Trigger
G.setup(GPIO_ECHO,G.IN)      # Echo



def on_connect(client,userData, flags,rc):
    print("Connected with result code " + str(rc))
    client.subscribe("topic/test")
    
def on_publish(mosq, userdata, mid):
    print("Image Sent")
    mosq.disconnect()
    
def on_message(client, userdata, msg):
    reply=msg.payload.decode()
    if reply=="YES":
        G.output(16,True)
        time.sleep(0.4)
        G.output(16,False)
        time.sleep(0.4)
        G.output(16,True)
        time.sleep(0.4)
        G.output(16,False)
        lcd.cursor_pos = (1, 8)
        lcd.write_string('YES')
        time.sleep(5)
        opengate()
        lcd.clear()
    elif reply=="NO":
        print("Unauthorized Car")
        time.sleep(0.4)
        G.output(16,True)
        time.sleep(0.4)
        G.output(16,False)
        time.sleep(0.4)
        G.output(16,True)
        time.sleep(0.4)
        G.output(16,False)
        lcd.cursor_pos = (1, 8)
        lcd.write_string('NO')
        time.sleep(5)
        lcd.clear()
        time.sleep(50)
                    
    client.disconnect()
    
def capture():
    call(["fswebcam", "-d","/dev/video0", "-r", "1280*720", "--no-banner", "./output.jpg"] )
    print("Image Clicked")
    
def opengate():
        p = G.PWM(12, 50)
        p.start(2.5)
        p.ChangeDutyCycle(8.5)  # turn towards 90 degree
        time.sleep(5) # sleep 1 second
        p.ChangeDutyCycle(2.5)  # turn towards 0 degree
        time.sleep(1) # sleep 1 second

lcd = CharLCD(cols=16 , rows=2 , pin_rs=37 , pin_e=35 , pins_data=[33, 31, 29, 23] , numbering_mode=G.BOARD)

    

if __name__=="__main__":
    while True:
        try:
            client=mqtt.Client()
            client.username_pw_set("bcyxgncf","ONqRG8casG5J")
            client.connect("farmer.cloudmqtt.com",13723,60)
            client.on_publish = on_publish
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
                
                if distance > 0 and distance < 100:
                    print "Distance:",distance - 0.5,"cm"
                    print("Obstacle detected")
                    G.output(16,True)
                    #client.publish("test","detected")
                    time.sleep(1)
                    G.output(16,False)
                    capture()
                    
                    f=open("output.jpg", "rb") #3.7kiB in same folder
                    fileContent = f.read()
                    byteArr = bytearray(fileContent)
                    client.publish("Image",byteArr,0)
                    client.loop_forever()
                    time.sleep(10)
                    
                    client.connect("farmer.cloudmqtt.com",13723,60)
                    client.on_connect = on_connect
                    client.on_message = on_message
                    client.loop_forever()
                    
                    
                    client.connect("farmer.cloudmqtt.com",13723,60)
                    
                else: 
                    print "Out Of Range"
                    time.sleep(1)

                                                   
                        
        except:
            G.cleanup()
            client.disconnect()
