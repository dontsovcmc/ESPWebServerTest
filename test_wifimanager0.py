
import os
import time
from requests import Session
from wifiadapter import WiFiAdapter
import pytest
import difflib

from bs4 import BeautifulSoup

from logger import log, PROJ_DIR, LOG_DIR, base_name


TMPL_DIR = os.path.join(PROJ_DIR, 'templates')

#TODO time .2

@pytest.fixture()
def ssid(pytestconfig):
    return pytestconfig.getoption("ssid")


@pytest.fixture()
def channel(pytestconfig):
    return pytestconfig.getoption("channel")


@pytest.fixture()
def ini(pytestconfig):
    return pytestconfig.getoption("ini")


@pytest.fixture()
def project(pytestconfig):
    return pytestconfig.getoption("project")


def test_compile():
    p


@pytest.fixture(scope="module")
def session():
    """
    HTTP request session
    """
    yield Session()


@pytest.fixture(scope="module")
def adapter():
    """
    Control notebook Wi-Fi adapter
    """
    yield WiFiAdapter()


def check_content(output, templ_name):
    """
    TODO: check ydiff utility
    """

    file_path = os.path.join(TMPL_DIR, templ_name)

    with open(file_path, 'r') as f:
        tmpl = f.readlines()
        output = output.splitlines()

        diff = difflib.unified_diff(tmpl, output)
        if '\n'.join(diff):
            diff = difflib.HtmlDiff().make_file(tmpl, output, '', '', context=True, numlines=3)
            with open(os.path.join(LOG_DIR, base_name + '_diff_' + templ_name), 'w') as f:
                f.write(diff)

            return False
        return True


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
    assert check_content(ret.text, 'index.html')


def test_wifi0(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/0wifi?')
    assert ret.ok
    log.info('/0wifi response: {} sec'.format(time.time() - t))
    assert check_content(ret.text, 'wifi0.html')


def test_i(session):
    t = time.time()
    ret = session.get('http://192.168.4.1/i?')
    assert ret.ok
    log.info('/i response: {} sec'.format(time.time() - t))

    soup = BeautifulSoup(ret.text, "html.parser")

    dl = soup.find('dl')

    def value(tag, key):
        dt = tag.find(name='dt', string=key)
        return str(dt.next_element.next_element.next_element)

    log.info('Chip ID: {}'.format(value(dl, 'Chip ID')))
    flash_size = int(value(dl, 'IDE Flash Size').split(' ')[0])
    log.info('IDE Flash Size: {}'.format(flash_size))
    assert flash_size > 0, 'incorrect flash_size'

    assert '192.168.4.1' == value(dl, 'Soft AP IP')



