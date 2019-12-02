

def pytest_addoption(parser):
    parser.addoption("--ssid", action="store", help="WiFiManager AP name")
    parser.addoption("--channel", action="store", default=1, type=int, help="WiFiManager AP channel")
    parser.addoption("--ini", action="store", help="path to platformio.ini file")
    parser.addoption("--project", action="store", help="path to source project")
