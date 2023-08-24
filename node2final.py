import RPi.GPIO as GPIO
import Adafruit_MCP3008
import adafruit_dht
import time
import board
import json
import paho.mqtt.client as mqtt
import datetime 

# SensorData class to store sensor readings
class SensorData:
    def __init__(self):
        self.moisture = 0
        self.gas = 0
        self.temperature = 0
        self.humidity = 0

# MQTTClientWrapper class to handle MQTT connection and publish messages
class MQTTClientWrapper:
    def __init__(self, broker, port, access_token=None):
        self.client = mqtt.Client()
        if access_token:
            self.client.username_pw_set(access_token)
        self.client.connect(broker, port, 60)
        self.client.loop_start()

    def publish_message(self, topic, message):
        self.client.publish(topic, message, 1)

    def cleanup(self):
        self.client.loop_stop()
        self.client.disconnect()

# SensorNode class to manage sensor data and publish it to ThingsBoard
class SensorNode:
    def __init__(self, thingsboard_broker, thingsboard_port, access_token, mqtt_broker, mqtt_port, mqtt_topic):
        self.mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)
        self.dht_device = adafruit_dht.DHT11(board.D4, use_pulseio=False)
        self.sensor_data = SensorData()
        self.thingsboard_mqtt_client = MQTTClientWrapper(thingsboard_broker, thingsboard_port, access_token)
        self.mqtt_client = MQTTClientWrapper(mqtt_broker, mqtt_port)
        self.mqtt_topic = mqtt_topic

    def read_moisture(self):
        moisture_value = self.mcp.read_adc(0)
        pmoist = moisture_value * 100 / 1023
        self.sensor_data.moisture = pmoist

    def read_gas(self):
        gas = self.mcp.read_adc(1)
        pgas = gas * 100 / 1023
        self.sensor_data.gas = pgas

    def read_temperature_humidity(self):
        try:
            humidity, temperature = self.dht_device.humidity, self.dht_device.temperature
            if humidity is not None:
                humidity = round(humidity, 2)
                self.sensor_data.humidity = humidity
            else:
                self.sensor_data.humidity = 0

            if temperature is not None:
                temperature = round(temperature, 2)
                self.sensor_data.temperature = temperature
            else:
                self.sensor_data.temperature = 0

        except RuntimeError as e:
            print("Error reading DHT11 sensor:", str(e))
            self.sensor_data.humidity = 0
            self.sensor_data.temperature = 0

    def publish_sensor_data(self):
        payload = {
            'ts':  int(datetime.datetime.now().timestamp() * 1000) ,
            'ref': 'Node2',
            'values': {
                'moisture': self.sensor_data.moisture,
                'gas': self.sensor_data.gas,
                'temperature': self.sensor_data.temperature,
                'humidity': self.sensor_data.humidity
            }
        }
        message = json.dumps(payload)
        self.thingsboard_mqtt_client.publish_message('v1/devices/me/telemetry', message)
        self.mqtt_client.publish_message(self.mqtt_topic, message)

    def control_gpio(self, pin, status):
        GPIO.output(pin, GPIO.HIGH if status else GPIO.LOW)

    def run(self, interval):
        next_reading = time.time()
        try:
            while True:
                self.read_moisture()
                self.read_gas()
                self.read_temperature_humidity()
                self.publish_sensor_data()

                # Perform GPIO control based on sensor data
                # Example: Turn on GPIO 7 (GPIO4 on BCM) if gas level is above 50%
                if self.sensor_data.gas > 50:
                    self.control_gpio(7, True)
                else:
                    self.control_gpio(7, False)

                time.sleep(interval)
        except KeyboardInterrupt:
            pass

    def cleanup(self):
        GPIO.cleanup()
        self.thingsboard_mqtt_client.cleanup()
        self.mqtt_client.cleanup()

if __name__ == "__main__":
    #Enter Devices details 
    THINGSBOARD_BROKER = "172.27.251.86"
    THINGSBOARD_PORT = 1883
    ACCESS_TOKEN = "smartgarden2"
    MQTT_BROKER = "172.27.251.86"
    MQTT_PORT = 1884
    MQTT_TOPIC = "mytopic1"

    node = SensorNode(THINGSBOARD_BROKER, THINGSBOARD_PORT, ACCESS_TOKEN, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)
    node.run(1)
    node.cleanup()
