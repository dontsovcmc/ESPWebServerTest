
from executor import execute
from bs4 import BeautifulSoup

from logger import log

#TODO: - linux support
#      - create pip package


class WiFiInfo:
    """
    Wi-Fi network description
    """
    def __init__(self):
        self.ssid = None
        self.bssid = None
        self.rssi = None
        self.channel = None

    def __str__(self):
        return self.ssid + '\t(' + str(self.rssi) + ') ' + '\tch=' + str(self.channel)


class WiFiAdapter:
    """
    Control your notebook Wi-Fi adapter.

    MacOS: https://www.mattcrampton.com/blog/managing_wifi_connections_using_the_mac_osx_terminal_command_line

    Linux: not supported

    Win: not supported
    """

    def __init__(self, device_name='en0'):
        self._d = device_name

        #MacOS
        self._airport_path = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'

    def on(self):
        """
        Turn on Wi-Fi adapter
        """
        return execute('networksetup -setairportpower {} on'.format(self._d))

    def off(self):
        """
        Turn off Wi-Fi adapter
        """
        return execute('networksetup -setairportpower {} off'.format(self._d))

    def is_on(self):
        """
        Check Wi-Fi adapter is on (powered)
        """
        return ': On' in execute('networksetup -getairportpower {}'.format(self._d), capture=True)

    def connect(self, ssid, pwd=''):
        """
        Connect to Wi-Fi network
        """
        r = execute('networksetup -setairportnetwork {} {} {}'.format(self._d, ssid, pwd), capture=True)
        if 'Failed to join network' in r:
            log.error(r)
            return False
        if 'Could not find network' in r:
            log.error(r)
            return False
        return r == ''

    def list(self):
        """
        Scan Wi-Fi networks and return list of them
        """
        out = execute('{} -s -x'.format(self._airport_path),
                      capture=True)
        soup = BeautifulSoup(out, "lxml")

        dicts = soup.find('array').findAll('dict', recursive=False)

        log.info('Found {} networks'.format(len(dicts)))

        ret = []
        for d in dicts:
            def value(tag, key):
                k = tag.findAll(name='key', string=key)[0]
                return k.next_element.next_element.next_element.string

            i = WiFiInfo()
            i.ssid = value(d, 'SSID_STR')
            i.bssid = value(d, 'BSSID')
            i.rssi = value(d, 'RSSI')
            i.channel = value(d, 'CHANNEL')
            ret.append(i)

        return ret

    def _parse_lines(self, out, key):
        out = [l.strip() for l in out.split('\n')]
        line = [l for l in out if l.startswith(key)]
        return line[0][len(key):]

    def current(self):
        """
        Connected Wi-Fi network info

        return WiFiInfo object
        """
        out = execute('{} -I'.format(self._airport_path),
                      capture=True)

        i = WiFiInfo()
        i.ssid = self._parse_lines(out, 'SSID: ')
        i.bssid = self._parse_lines(out, 'BSSID: ')
        i.rssi = self._parse_lines(out, 'agrCtlRSSI: ')
        i.channel = int(self._parse_lines(out, 'channel: '))

        return i

    def ip(self):
        """
        Current ip
        """
        out = execute('networksetup -getinfo Wi-Fi', capture=True)
        return self._parse_lines(out, 'IP address: ')

    def router(self):
        """
        Current router ip
        """
        out = execute('networksetup -getinfo Wi-Fi', capture=True)
        return self._parse_lines(out, 'Router: ')


    @staticmethod
    def interfaces():
        """
        Available interfaces
        """
        print(execute('networksetup -listallhardwareports', capture=True))


wc = WiFiAdapter()
