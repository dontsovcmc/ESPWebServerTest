
from logger import log

from compile import project_dir, project_conf, lib, upload_port, noupload, compile


def test_example(setup):
    log.info('Test ESP here')
    assert True
