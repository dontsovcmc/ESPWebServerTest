
# Test ESP WebServer by Python scripts

With this library you can:

- build firmware using Platformio 
- upload firmware using Platformio

- connect to ESP8266/ESP32 Active Point
- execute HTTP requests
- compare web page content with templates


limitation: Only MacOS Wi-Fi adapter support. Please open an issues with your Wi-Fi adapter info.

## Quick start
1. install requirements by `pip install -r requirements.txt`
2. call `$ pytest --noupload`


## Using
1. create test_*.py files with your tests
2. run `pytes` with options

### pytest arguments
for compile firmware
- --lib - path to library you want to use
- --dir - path to folder with firmware source files
- --conf - path to platformio.ini file. if None use default
- --port - upload port 
- --noupload - skip compiling and uploading firmware

for test chip
- --ssid - chip SSID name
- --channel - chip Wi-Fi channel

## Example

We have:
```
/Documents/WiFiManager
/Documents/MyProject/src/main.cpp
/Documents/MyProject/platformio.ini

/Documents/ESPWebServerTest/test_my_project.py

```

Call:
`pytest --lib=/Documents/WiFiManager --dir=/Documents/YourProject --port=/dev/cu.SLAB_USBtoUART`

1. move /Documents/MyProject to /Documents/ESPWebServerTest/sandbox
2. move /Documents/WiFiManager to /Documents/ESPWebServerTest/sandbox/lib
3. platformio run --target upload --upload-port /dev/cu.SLAB_USBtoUART
4. call all test_ functions in test_my_project.py

Profit!



