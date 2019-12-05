
import os
import time
from bs4 import BeautifulSoup
from logger import log

TMPL_DIR = os.path.join(os.path.dirname(__file__), 'html')

#TODO time .2


from compile import project_dir, project_conf, lib, upload_port, noupload, compile
from compile import ssid, channel
from adapter import session, adapter
from utils import diff_html


def test_compile(compile):
    pass


def test_connect(ssid, adapter):
    if adapter.current().ssid == ssid:
        log.info('Already connected, skip')
        return

    log.info('Connecting to WifiManager AP: {}'.format(ssid))

    t = time.time()
    assert adapter.connect(ssid)
    log.info('Connecting time: {} sec'.format(time.time() - t))


def test_wifi_settings(ssid, channel, adapter):
    i = adapter.current()
    assert i.ssid == ssid
    assert i.channel == channel
    log.info('RSSI: {}'.format(i.rssi))


def test_index(session):
    t = time.time()
    ret = session.get('http://192.168.4.1')
    assert ret.ok
    log.info('Root response: {} sec'.format(time.time() - t))
    assert diff_html(ret.text, TMPL_DIR, 'index.html')


def test_wifi0(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/0wifi?')
    assert ret.ok
    log.info('/0wifi response: {} sec'.format(time.time() - t))
    assert diff_html(ret.text, TMPL_DIR, 'wifi0.html')


def test_i(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/i?')
    assert ret.ok
    log.info('/i response: {} sec'.format(time.time() - t))

    soup = BeautifulSoup(ret.text, 'html.parser')

    dl = soup.find('dl')

    def value(tag, key):
        dt = tag.find(name='dt', string=key)
        return str(dt.next_element.next_element.next_element)

    log.info('Chip ID: {}'.format(value(dl, 'Chip ID')))
    flash_size = int(value(dl, 'IDE Flash Size').split(' ')[0])
    log.info('IDE Flash Size: {}'.format(flash_size))
    assert flash_size > 0, 'incorrect flash_size'

    assert '192.168.4.1' == value(dl, 'Soft AP IP')



