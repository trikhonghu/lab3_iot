import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *
from uart import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "vantri15042003"
AIO_KEY = "aio_HgTx27tR4yLkGKlvbozdAyUInYXi"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + ", feed id: " + feed_id)
    if feed_id == "nutnhan1":
        if payload == "0":
            writeData("nut1 tat\n")
        else:
            writeData("nut1 bat\n")
    if feed_id == "nutnhan2":
        if payload == "0":
            writeData("nut2 tat\n")
        else:
            writeData("nut2 bat\n")

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 5

ai_res = ""
prev_ai_res = ""

while True:
    counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        prev_ai_res = ai_res
        ai_res = image_detector()
        if ai_res != prev_ai_res :
            print(ai_res)
            client.publish("ai" , ai_res)
    
    readSerial(client)
    # # Listen to the keyboard for presses.
    # keyboard_input = cv2.waitKey(1)

    # # 27 is the ASCII for the esc key on your keyboard.
    # if keyboard_input == 27:
    #     break
    time.sleep(1)
    pass