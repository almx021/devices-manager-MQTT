import paho.mqtt.client as mqtt


class EquipmentManager:
    def __init__(self, host="localhost", port=1883):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)
        try:
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("FINISHING APPLICATION")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the broker. Press CTRL+C to stop")
            client.subscribe("#")

    def on_message(self, client, data, message):
        print(f"ALERT [{message.topic}]: {message.payload.decode()}")

if __name__ == '__main__':
    from sys import argv
    host = None
    port = None
    if len(argv) > 2:
        host = argv[1]
        port = argv[2]
        EquipmentManager(host, port)
    else:
        EquipmentManager()