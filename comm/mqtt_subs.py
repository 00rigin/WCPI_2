import paho.mqtt.client as mqtt
import json
from collections import OrderedDict
import codecs
import numpy as np
import time
import queue
import threading

with open('config.json', 'r') as f:
        config = json.load(f)

#import cv2 as cv
# MQTT 설정
#MQTT_Broker = "223.194.33.80"
#MQTT_Broker = "192.168.0.102"
MQTT_Broker = config['DEFAULT']['IP_ADD']
MQTT_Port = config['DEFAULT']['PORT_NUM']
Keep_Alive_Interval = 100
#MQTT_Topic = "camera/cam2"
#MQTT_Topic_pi = "cluster/#"
MQTT_Topic_pi = "cluster/#"

mqttc = mqtt.Client()

array = []
class buffer:
    def get_list(self):
        global array
        return array
   
#브로커와 연결됐는지 확인
def on_connect(mosq, obj, rc):
   if rc == 0:
      print("connected with result code " + str(rc))
      #mqttc.subscribe((MQTT_Topic_pi,0))
      #mqttc.subscribe(MQTT_Topic_pi,0)
      #mqttc.subscribe((MQTT_Topic_pi2,0))
      #mqttc.subscribe((MQTT_Topic_srv,0))
   #mqttc.subscribe(MQTT_Topic, 0)

#데이터 DB에 저장
def on_message(mosq, obj, msg):
   print("MQTT Data Received...")
   print("MQTT Topic: " + msg.topic )
   
   data = msg.payload.decode("utf-8")
   json_load = json.loads(data)
   array.append(json_load)
   

def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(mosq, obj, mid, granted_qos):
   print("subscribed:" +str(mid) + " "+ str(granted_qos))
   

#mqttc = mqtt.Client()
#mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
#mqttc.on_message = functools.partial(mess,

#연결
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe((MQTT_Topic_pi,0))
# 네트위크 이벤트 루푸를 지속시킨다
mqttc.loop_start()

#sub = threading.Thread(target=subscribing)
#pub = threading.Thread(target=main)
#sub.start()
#pub.start()