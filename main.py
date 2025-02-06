from tkinter import scrolledtext

import paho.mqtt.client as mqtt
import tkinter as tk


class EquipmentManager:
    def __init__(self, root: tk.Tk, host="localhost", port=1883):
        self.root = root
        self._configure_window()

        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(host, port)

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to the broker")
            client.subscribe("#")
        else:
            print("Failed to connect properly")
            self.root.quit()
            self.root.destroy()

    def on_message(self, client, data, message):
        topic = message.topic
        alert_time, message_value = message.payload.decode().split('//')
        
        if message_value == 'DISCONNECTED':
            if topic not in self.topic_array:
                return
            self.topic_array.remove(topic)
            self.update_topic_list()
        elif topic not in self.topic_array:
            self.topic_array.append(topic)
            self.update_topic_list()

        self.message_box.config(state='normal')
        self.message_box.insert(tk.END, f"[{alert_time}] - {topic}: {message_value}\n")
        self.message_box.config(state='disabled')
        self.message_box.yview(tk.END)

    def _configure_window(self):
        self.root.title("MQTT Equipments manager")
        self.root.geometry("800x500")

        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH)

        frameListBox = tk.Frame(frame)
        frameListBox.pack(side=tk.LEFT, fill=tk.Y)

        labelListBox = tk.Label(frameListBox, text="TOPICS")
        labelListBox.pack(side=tk.TOP, fill=tk.Y)

        self.topic_array = []
        self.topic_list = tk.Listbox(frameListBox, width=30, height=28)
        self.topic_list.pack(side=tk.TOP, fill=tk.Y, padx=10, pady=10)

        frameMessageBox = tk.Frame(frame)
        frameMessageBox.pack(side=tk.RIGHT, fill=tk.BOTH)

        labelMessageBox = tk.Label(frameMessageBox, text='ALERTS')
        labelMessageBox.pack(side=tk.TOP, fill=tk.Y)

        self.message_box = scrolledtext.ScrolledText(frameMessageBox, width=400, height=28)
        self.message_box.pack(side=tk.TOP, fill=tk.BOTH,  padx=10, pady=10)
        self.message_box.config(state='disabled')

    def update_topic_list(self):
        self.topic_list.delete(0, tk.END)
        for topic in self.topic_array:
            self.topic_list.insert(tk.END, topic)

if __name__ == '__main__':
    root = tk.Tk()

    from sys import argv
    host = None
    port = None
    if len(argv) > 2:
        host = argv[1]
        port = argv[2]
        EquipmentManager(root, host, port)
    else:
        EquipmentManager(root)

    root.mainloop()