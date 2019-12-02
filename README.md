

ESP WebServer test framework: 

- connect to ESP8266/ESP32 Active Point
- HTTP requests
- compare web page content with templates


## Run
1. upload target firmware to ESP
2. create test_*.py file with tests
3. reset ESP
4. run 'pytest'


## Example
pytest --ssid <ESP ssid>