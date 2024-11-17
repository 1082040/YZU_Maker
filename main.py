*from tkinter import *
from tkinter import ttk
from tkinter import font
import RPi.GPIO as GPIO
import time
import random
import datetime
import subprocess
import requests
import math
import Adafruit_DHT
from datetime import date
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
TOKEN = "BBFF-PMEIayHfp8F5hONW1GmgOcw9wv10RM"  # Put your TOKEN here ubidots
DEVICE_LABEL = "temperature"  # Put your device label here 
VARIABLE_LABEL_1 = "tmp"  # Put your first variable label here
VARIABLE_LABEL_2 = "hmd"  # Put your second variable label here
VARIABLE_LABEL_3 = "pos"  # Put your second variable label here

pins = (11,12,13) 
global pwmR, pwmG, pwmB
pressed=0
GPIO.setmode(GPIO.BOARD)
# iterate on the RGB pins, initialize each and set to HIGH to turn it off 
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
BTN_PIN = 15 #button pin
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def build_payload(variable_1, variable_2, variable_3):# the code for output the temperature and humidity 
    # Creates two random values for sending data
    global tem1, hum1
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        print("Temp={0:0.2f}*C  Humidity={1:0.2f}%".format(temperature, humidity))
        value_1 = temperature
        value_2 = humidity
        tem1 = temperature
        hum1 = humidity
    else:
        tem1 = 0
        hum1 = 0
        value_1 = 0
        value_2 = 0
    # Creates a random gps coordinates
    lat = random.randrange(34, 36, 1) + \
        random.randrange(1, 1000, 1) / 1000.0
    lng = random.randrange(-83, -87, -1) + \
        random.randrange(1, 1000, 1) / 1000.0
    payload = {variable_1: value_1,
               variable_2: value_2,
               variable_3: {"value": 1, "context": {"lat": lat, "lng": lng}}}
    return payload

def post_request(payload):# for sending information to ubidots
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)
    # Processes results
    if status >= 400:
            #your token credentials and internet connection")
        return False
    return True

def mmm():# for send the data to VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3
    payload = build_payload(
        VARIABLE_LABEL_1, VARIABLE_LABEL_2, VARIABLE_LABEL_3)
    post_request(payload)
    
def destroy():# the end funtion1
    pwmR.stop()
    pwmG.stop()
    pwmB.stop()
    pwmR.start(0)   # initially set to 0 duty cycle
    pwmG.start(0)
    pwmB.start(0)
    setColor(100,100,100)
    GPIO.cleanup()
   
def quit(*args):    # the end funtion2
    destroy()
    root.destroy()
    
def show_time():#output time in the screen
    
    # Get the time remaining until the event
    remainder = endTime - datetime.datetime.now()
    # remove the microseconds part
    remainder = remainder - datetime.timedelta(microseconds=remainder.microseconds)
    # Show the time left
    displayColors(remainder.days)
    #testtxt=[remainder]
    testtxt=[remainder,'tem:',tem1,'°C,hum:',hum1,'%']
    #mmm()
    txt.set(testtxt)
    # Trigger the countdown after 1000ms    
    root.after(1000, show_time)
    
def ButtonPressed(btn):     #funtion for the button to start and end the screen
    global pressed
    if pressed==0:
        pressed=1
        time.sleep(0.1)
    elif pressed==1:
        pressed=0
        destroy()
        root.destroy()
    return pressed
    # Use tkinter lib for showing the clock
       
def displayColors(x):       
    if x>=0 and x<=7:
        setColor(100, 0, 100) # green
         #if the day is between 0 to 7 days show color green
    elif x<0:
        setColor(0, 100, 100) # red
        #if less than 0 day less than show red
    elif x>7:
        setColor(100, 100, 0) # blue
        #if day is larger than 7 days show color blue 

     
def setColor(r, g, b):  
    pwmR.ChangeDutyCycle(r)  #led red
    pwmG.ChangeDutyCycle(g)  #led green
    pwmB.ChangeDutyCycle(b)  #led blue
     
if __name__ == '__main__':
    
    pwmR = GPIO.PWM(pins[0], 100)  # set each PWM pin to 2 KHz
    pwmG = GPIO.PWM(pins[1], 100)
    pwmB = GPIO.PWM(pins[2], 100)
    pwmR.start(0)   # initially set to 0 duty cycle
    pwmG.start(0)
    pwmB.start(0)
    setColor(100,100,100)
    , BuGPIO.add_event_detect(BTN_PIN, GPIO.FALLINGttonPressed, 200)#set button and led
    global year1,month1,date1        #set the time you gonna set
    print("input year")
    year1=int(input())
    print("input month")
    month1=int(input())
    print("input date")
    date1=int(input())
    root = Tk()
    print("run")
    while pressed==0:
        time.sleep(0.1)
    if pressed==1:
        time.sleep(0.1)
        root.attributes("-fullscreen", True)# the window in full screen
        root.configure(background='black')  # the backgroung is black
        root.bind("x", quit)                # if press x quit
        root.after(1000, show_time)         # show the time after 1 seconds

        # Set the end date and time for the countdown
        endTime = datetime.datetime(year1, month1, date1, 0, 0 ,0)
                          
        fnt = font.Font(family='Helvetica', size=25, weight='bold') # the word format
        txt = StringVar()
        lbl = ttk.Label(root, textvariable=txt, font=fnt, foreground="white", background="black")
        lbl.place(relx=0.5, rely=0.5, anchor=CENTER)#output format
        mmm() 
        root.mainloop()*# keep in new time on screen 