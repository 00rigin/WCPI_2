"""
Some boilerplate code to handle MQTT.
"""
import paho.mqtt.client as mqtt
import time

MQTT_Broker = "192.168.137.222"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "camera/image"

# Reqired callbacks
def on_connect(client, userdata, flags, rc):
    # print(f"CONNACK received with code {rc}")
    if rc == 0:
        print("connected to MQTT broker")
        client.connected_flag = True  # set flag
    else:
        print("Bad connection to MQTT broker, returned code=", rc)


def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass
    
def get_mqtt_client():
    """Return the MQTT client object."""
    client = mqtt.Client()
    client.connected_flag = False  # set flag
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.connect(MQTT_Broker, port=MQTT_Port)
    time.sleep(2)
    client.loop_start()
    return client

def publish_msg(client, message):
    cli = client
    infot = cli.publish(MQTT_Topic,message,0)
    infot.wait_for_publish()
    print("finish publish")