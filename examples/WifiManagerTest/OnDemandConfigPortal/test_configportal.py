
import os
import sys
import time
from bs4 import BeautifulSoup
from logger import log
import pytest

TMPL_DIR = os.path.join(os.path.dirname(__file__), 'html')

#TODO time .2


from build import project_dir, project_conf, lib, upload_port, build, build_and_upload
from build import ssid, channel
from adapter import session, adapter
from utils import diff_html


def test_init(build_and_upload):
    """
    Using compile argument emit run fixture that compiles and upload firmware
    """
    pass


def test_connect(ssid, adapter):
    if adapter.current().ssid == ssid:
        log.info('Already connected, skip')
        return

    assert adapter.wait_network(ssid), 'AP isn\'t found'

    log.info('Connecting to WifiManager AP: {}'.format(ssid))

    t = time.time()
    if not adapter.connect(ssid):
        pytest.exit('Failed to connect', 1)
    log.info('Connecting time: {} sec'.format(time.time() - t))


def test_wifi_settings(ssid, channel, adapter):
    i = adapter.current()
    assert i.ssid == ssid
    assert int(i.channel) == channel
    log.info('RSSI: {}'.format(i.rssi))


def test_index(session):
    t = time.time()
    ret = session.get('http://192.168.4.1')
    assert ret.ok
    log.info('Root response: {} sec'.format(time.time() - t))
    assert diff_html(ret.text, TMPL_DIR, 'i.html')


def test_wifi0(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/0wifi?')
    assert ret.ok
    log.info('/0wifi response: {} sec'.format(time.time() - t))
    assert diff_html(ret.text, TMPL_DIR, 'wifi0.html')


def test_param(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/param')
    assert ret.ok
    log.info('/param response: {} sec'.format(time.time() - t))

    assert diff_html(ret.text, TMPL_DIR, 'param.html')

    soup = BeautifulSoup(ret.text, 'html.parser')

    server = soup.find('input', {'id': 'server'}).get('value')
    assert server == ''

    #save param manually

    data = {
        'server': 'some_url'
    }

    ret = session.post('http://192.168.4.1/paramsave', data=data)
    assert diff_html(ret.text, TMPL_DIR, 'paramsave.html')


    ret = session.get('http://192.168.4.1/param')

    soup = BeautifulSoup(ret.text, 'html.parser')

    server = soup.find('input', {'id': 'server'}).get('value')
    assert server == 'some_url'
