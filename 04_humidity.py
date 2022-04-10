from paho.mqtt.client import Client
import sys

TEMP = "temperature"
HUMIDITY = "humidity"

def on_message(mqttc, data, msg):
    print ("message:{}:{}:{}".format(msg.topic,msg.payload,data))
    if data["status"] == 0:
        temp = int(msg.payload)
        if temp > data["temp_threshold"]:
            print("umbral superado {}, suscribiendo a humidity".format(temp))
            mqttc.subscribe("HUMIDITY")
            data["status"] = 1
    elif data["status"] == 1:
        if msg.topic == HUMIDITY:
            humidity = int(msg.payload)
            if humidity > data["humidity_threshold"]:
                print("umbral humedad {} superado, cancelando suscripción".format(humidity))
                mqttc.unsubscribe(HUMIDITY)
                data["status"] = 0
        elif TEMP in msg.topic:
            temp = int(msg.payload)
            if temp <= data["temp_threshold"]:
                print("temperatura {} por debajo de umbral, cancelando suscripción".format(temp))
                data["status"]=0
                mqttc.unsubscribe(HUMIDITY)

def on_log(mqttc, data, level, buf):
    print("LOG: {}:{}".format(data,mqttc))

def main(broker):
    data = {"temp_threshold":20,"humidity_threshold":80,"status": 0}
    mqttc = Client(userdata = data)
    mqttc.on_message = on_message
    mqttc.enable_logger()
    mqttc.connect(broker)
    mqttc.subscribe("{}/t1".format(TEMP))
    mqttc.loop_forever()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} broker".format(sys.argv[0]))
        sys.exit(1)
    broker = sys.argv[1]
    main(broker)
