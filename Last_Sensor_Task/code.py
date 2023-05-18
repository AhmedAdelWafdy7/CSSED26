import RPi.GPIO as GPIO
import time
import LCD
import UltraSonic
lcd = LCD(rs=37, en=35, d4=33, d5=31, d6=29, d7=23)
US = UltrasonicSensor(trigger_pin=16, echo_pin=18)
sensor = 16
led = 11
buzzer = 12 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(led,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

p = GPIO.PWM(led,50)

p.start(5)

while(True):
    distance = sensor.get_distance()
    lcd.write_line(0, "Distance :{distance}")
    US.cleanup()
    if GPIO.input(sensor):
        GPIO.output(buzzer, True)
        lcd.write_line(1, "Object detected")
    else :
        GPIO.output(buzzer, False)
        lcd.write_line(1, "Not detected")            
    if distance > 3 :
        p.ChangeDutyCycle(120*100/255)
        p.ChangeDutyCycle(80*100/255)
        p.ChangeDutyCycle(70*100/255)
        time.sleep(2)
    else :
        p.ChangeDutyCycle(200*100/255)
        p.ChangeDutyCycle(100*100/255)
        p.ChangeDutyCycle(50*100/255)
        time.sleep(2)    
         