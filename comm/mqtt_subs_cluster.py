import paho.mqtt.client as mqtt
import json
from collections import OrderedDict
import codecs
import numpy as np
#import cv2 as cv
# MQTT 설정
MQTT_Broker = "127.0.0.1"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "camera/"
#MQTT_Topic = [("camera/cluster",0),("camera/image",0)]
#MQTT_Topic_pi = "camera/cluster"
#MQTT_Topic_srv = "camera/image"
mqttc = mqtt.Client()
#브로커와 연결됐는지 확인
def on_connect(mosq, obj, rc):
   if rc == 0:
      print("connected with result code " + str(rc))
      #mqttc.subscribe((MQTT_Topic_pi,0))
      #mqttc.subscribe((MQTT_Topic_srv,0))
   #mqttc.subscribe(MQTT_Topic, 0)

#데이터 DB에 저장
def on_message(mosq, obj, msg):
   print("MQTT Data Received...")
   print("MQTT Topic: " + msg.topic )
   #print("Data: " + str(msg.payload.decode("utf-8")))
   data = msg.payload.decode("utf-8")
   json_load = json.loads(data)
   
   
   # 20200603 data that sending to pi
   p_id_restored = int(json_load['p_id'])
   f_cluster_mat_restored = np.array(json_load['f_cluster_mat'], dtype = np.float32)
   avg_feature_restored = np.array(json_load['avg_feature'], dtype = np.float32)
   
   
   
   print("******************************")
   print("p_id : ", p_id_restored)
   print("f_cluster_mat_restored : ", f_cluster_mat_restored)
   print("avg_feature_restored : ", avg_feature_restored)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))

def on_subscribe(mosq, obj, mid, granted_qos):
   print("subscribed:" +str(mid) + " "+ str(granted_qos))

#mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message


#연결
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe((MQTT_Topic,0))
# 네트위크 이벤트 루푸를 지속시킨다
mqttc.loop_forever()
