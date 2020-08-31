# Reqired callbacks

import paho.mqtt.client as mqtt
import json
import time

with open('config.json', 'r') as f:
        config = json.load(f)

MQTT_Broker = config['DEFAULT']['IP_ADD']
MQTT_Port = config['DEFAULT']['PORT_NUM']
Keep_Alive_Interval = 100
#MQTT_Topic = "camera/cam1"
#MQTT_Topic_pi = "cluster/cam2"
cli_num = str(config['DEFAULT']['CAM_ID'] + 1)
MQTT_Topic_pi1 = "cluster/cli" + cli_num
#MQTT_Topic_pi2 = "cluster/cli3"
MQTT_Topic_srv = "camera/cam" + cli_num

def on_connect(client, userdata, flags, rc):
    # print(f"CONNACK received with code {rc}")
    if rc == 0:
        print("connected to MQTT broker")
        client.connected_flag = True  # set flag
       
    else:
        print("Bad connection to MQTT broker, returned code=", rc)

def on_publish(client, userdata, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass

def initialize_mqtt():
    client = mqtt.Client()
    client.connected_flag = False  # set flag
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.connect(MQTT_Broker, port=MQTT_Port)
    time.sleep(2)
    client.loop_start()
    return client

def publish_msg_srv(client, message):
    cli = client
    #infot = cli.publish(MQTT_Topic,message,0)
    info_pic = cli.publish(MQTT_Topic_srv,message,0)
    #info_clus = cli.publish(MQTT_Topic_pi,message,0)
    #infot.wait_for_publish()
    info_pic.wait_for_publish()
    #info_clus.wait_for_publish()
    print("finish publish to srv")

def publish_msg_pi1(client, message):
    cli = client
    infot = cli.publish(MQTT_Topic_pi1,message,0)
    infot.wait_for_publish()
    print("finish publish to pi1")

def publish_msg_pi2(client, message):
    cli = client
    infot = cli.publish(MQTT_Topic_pi2,message,0)
    infot.wait_for_publish()
    print("finish publish to pi2")

def publish_msg(client, message):
    cli = client
    infot = cli.publish(MQTT_Topic,message,0)
    #infot = cli.publish.multiple(message,MQTT_Broker)
    infot.wait_for_publish()
    print("finish publish")