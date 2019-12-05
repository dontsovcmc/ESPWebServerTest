

def pytest_addoption(parser):

    parser.addoption("--ssid", action="store", help="WiFiManager AP name")
    parser.addoption("--channel", action="store", default=1, type=int, help="WiFiManager AP channel")
    parser.addoption("--port", action="store", help="upload port")
    parser.addoption("--conf", action="store", help="path to platformio.ini file")
    parser.addoption("--dir", action="store", help="path to folder with project files")
    parser.addoption("--lib", action="store", help="path to library your want to include")
    parser.addoption("--build", action="store_true", help="upload firmware to chip")
