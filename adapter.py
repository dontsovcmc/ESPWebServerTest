
import pytest
from requests import Session
from wifiadapter import WiFiAdapter


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
