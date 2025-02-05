import random
from threading import Lock, Event, Thread
from time import sleep

from paho.mqtt import client as mqtt

class Equipment:
    sensor_types = ('SPEED', 'TEMPERATURE', 'PRESSURE', 'HUMIDITY')
    
    def __init__(self, name: str, measurement_type: str, lower_limit: float, upper_limit: float, host="localhost", port=1883):
        if upper_limit <= lower_limit:
            raise ValueError

        self.lock = Lock()
        self.measurement_lock = Event()
        self.finish_lock = Event()

        self.power_on = False
        self.name = name
        self.sensor_type = measurement_type
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

        self.client = mqtt.Client(client_id=f"{self.sensor_type.capitalize()}Sensor/{self.name}")
        self.client.connect(host, port)

        user_input = ...
        while True:
            status = "STOP to stop the sensor" if self.power_on else "START to start the sensor"
            print(f"EQUIPMENT DATA:\n\tNAME: {self.name}\n\tSENSOR TYPE: {self.sensor_type}\n\tLIMITS: {self.lower_limit, self.upper_limit}")
            user_input = input(f"COMMANDS:\n\t{status}\n\tEXIT to stop the application\n").strip().upper()
            print()

            if user_input in ('START','STOP'):
                self.power()
            elif user_input == 'EXIT':
                with self.lock:
                    self.power_on = False
                if hasattr(self, 'measurement_thread'):
                    self.finish_lock.set()
                    self.measurement_lock.set()
                print("TURNING OFF")
                break


    def start_measurements(self):
        print('\nSTARTING MEASUREMENTS')
        while not self.finish_lock.is_set():
            self.measurement_lock.wait()
            if self.power_on:
                measurement = random.uniform(self.lower_limit - (0.2*self.lower_limit), self.upper_limit + (0.2*self.upper_limit))
                if self.lower_limit > measurement or measurement > self.upper_limit:
                    self.alert_manager(measurement)
                sleep(1)

    def power(self):
        with self.lock:
            self.power_on = not self.power_on
            if not self.power_on:
                print('\nPAUSING MEASUREMENTS')
                self.measurement_lock.clear()
            else:
                if hasattr(self, 'measurement_thread'):
                    self.measurement_lock.set()
                else:
                    self.measurement_lock.set()
                    self.measurement_thread = Thread(target=self.start_measurements, args=(), daemon=True)
                    self.measurement_thread.start()
            

    def alert_manager(self, measured_value):
        print(f"----------ALERT [{self.name}]: {measured_value}----------")
        r = self.client.publish(f"{self.client._client_id.decode()}", f"{measured_value}")
        if r.rc != 0:
            print('mensagem não enviada')

if __name__ == '__main__':
    from sys import argv

    name = input("Equipment name: ").strip().upper()
    type = input("Equipment type [SPEED, TEMPERATURE, PRESSURE or HUMIDITY]: ").strip().upper()
    if type not in Equipment.sensor_types:
        raise ValueError("Invalid Equipment type")
    lower_limit = float(input("Measurement range lower limit [integer or decimal]: "))
    upper_limit = float(input("Measurement range upper limit [integer or decimal]: "))

    host = None
    port = None
    if len(argv) > 2:
        host = argv[1]
        port = argv[2]
        Equipment(name, type, lower_limit, upper_limit, host, port)
    else:
        Equipment(name, type, lower_limit, upper_limit)