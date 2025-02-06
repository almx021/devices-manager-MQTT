# Equipments Manager - Message Oriented Middleware (MQTT)

# Requirements
- Python 3.12 or superior
- Paho-mqtt (run `pip install paho-mqtt`)
- Access to a mosquitto broker or running mosquitto docker image

# How to Run
**Disclaimer**: The keyword `python` must be understood as _the keyword to access python in your O.S._. For instance, if you are running `Debian`, it must be understood as `python3`

### With localhost:1883 broker:
- Open a terminal on root folder and run `python main.py`
- Open a terminal on root folder for every equipment, run `python equipment` in every terminal and follow the instructions
### With custom broker:
- Open a terminal on root folder and run `python main.py <broker address> <broker port>`
- Open a terminal on root folder for every equipment, run `python equipment <broker address> <broker port>` in every terminal and follow the instructions
## Stopping the application
- To finish the manager, just close its tkinter window. Keep in mind that it does not stops any equipments from running. Follow their instructions in order to deal with halting instruments measurements
