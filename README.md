# IOT-STREET-LIGHT-SIMULATION
Smart street lighting system using ESP8266/ESP32 and IR sensors to control lights based on vehicle detection. Data is monitored via ThingSpeak, while computer vision counts vehicles. Energy savings are estimated based on active lighting duration, making it an efficient solution for low-traffic areas.


Data on both files:
### vehicle_detection.py 
Python computer vision code for vehicle detection and ThingSpeak data transmission


### esp_street_light_control.ino 
ESP8266/ESP32 firmware for street light control and IoT integration

## REQUIREMENTS

#### Replace YOUR_SSID, YOUR_PASSWORD, YOUR_THINGSPEAK_API in ESP code
#### Replace YOUR_API_KEY in Python code
#### Install OpenCV: pip install opencv-python requests
