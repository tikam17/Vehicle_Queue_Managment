from RPLCD.gpio import CharLCD
import RPi.GPIO as G
import time
G.setwarnings(False)

lcd = CharLCD(cols=16 , rows=2 , pin_rs=37 , pin_e=35 , pins_data=[33, 31, 29, 23] , numbering_mode=G.BOARD)

while True:
    lcd.cursor_pos = (1, 8)
    lcd.write_string('NO')
    time.sleep(1)
    lcd.clear()
    time.sleep(1)
