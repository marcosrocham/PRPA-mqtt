from paho.mqtt.client import Client
from multiprocessing import Process, Manager
from time import sleep
import random
import sys

NUMBERS = "numbers"
CLIENTS = "clients"
TIMER_STOP = "{}/timerstop".format(CLIENTS)
HUMIDITY = "humidity"

def is_prime(n):
    i = 2
    while i*i < n and n % i != 0:
        i += 1
    return i*i > n

def timer(time, data):
    mqttc = Client()
    mqttc.connect(data["broker"])
    msg = "timer working. timeout: {}".format(time)
    print(msg)
    mqttc.publish(TIMER_STOP, msg)
    sleep(time)
    msg = "timer working. timeout: {}".format(time)
    mqttc.publish(TIMER_STOP, msg)
    print("timer end working")
    mqttc.disconnect()

def on_message(mqttc, data, msg):
    print("MESSAGE:data:{}, msg.topic:{}, payload:{}".format(data,msg.topic,msg.payload))
    try:
        if int(msg.payload) % 2 == 0:
            worker = Process(target=timer, args=(random.random()*20, data))
            worker.start()
    except ValueError as e:
        print(e)
        pass

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)

def main(broker):
    data = {"client":None,"broker": broker}
    mqttc = Client(userdata=data)
    data["client"] = mqttc
    mqttc.enable_logger()
    mqttc.on_message = on_message
    mqttc.on_log = on_log
    mqttc.connect(broker)
    mqttc.subscribe(NUMBERS)
    mqttc.loop_forever()
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} broker".format(sys.argv[0]))
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
