
import os
import glob
import shutil
import pytest
from executor import execute

from logger import log, PROJ_DIR


TMPL_DIR = os.path.join(PROJ_DIR, 'templates')

SANDBOX_DIR = os.path.join(PROJ_DIR, 'sandbox')
SRC_DIR = os.path.join(SANDBOX_DIR, 'src')
LIB_DIR = os.path.join(SANDBOX_DIR, 'lib')
UPLOAD_SKIP = os.path.join(SANDBOX_DIR, 'upload.skip')


@pytest.fixture(scope='session')
def upload_port(pytestconfig):
    return pytestconfig.getoption("port")


@pytest.fixture(scope='session')
def build(pytestconfig):
    return pytestconfig.getoption("build")


@pytest.fixture(scope='session')
def project_conf(pytestconfig):
    """
    Find platformio.ini file
    """
    # command line argument
    if pytestconfig.getoption("conf"):
        return pytestconfig.getoption("conf")

    # pytest run directory
    if os.path.isfile(os.path.join(pytestconfig.args[0], 'platformio.ini')):
        return os.path.join(pytestconfig.args[0], 'platformio.ini')

    # default
    return os.path.join(PROJ_DIR, 'platformio.ini')


@pytest.fixture(scope='session')
def project_dir(pytestconfig):
    return pytestconfig.getoption("dir")


@pytest.fixture(scope='session')
def lib(pytestconfig):
    return pytestconfig.getoption("lib", '')


@pytest.fixture(autouse=True, scope='session')
def build_and_upload(project_dir, project_conf, lib, upload_port, build):

    """
    Init sandbox: copy library and ino/cpp file
    """
    if not build:
        log.info('No upload, skip compile&upload')
        log.info('Reset chip')
        log.info(execute('python -m esptool --port {} --after hard_reset chip_id'.format(upload_port), capture=True))
        return

    if not project_dir:
        log.error('project_dir is required')
    if not upload_port:
        log.warning('no upload port defined')

    # clean
    if os.path.isdir(SANDBOX_DIR):
        shutil.rmtree(SANDBOX_DIR)
    os.mkdir(SANDBOX_DIR)
    if not os.path.isdir(SRC_DIR):
        os.mkdir(SRC_DIR)
    log.info('Folder cleaned')

    log.info('Platformio path: ' + execute('which platformio',
                                           directory=SANDBOX_DIR,
                                           capture=True))
    execute('platformio init',
            directory=SANDBOX_DIR,
            capture=True)

    # copy files to '/sandbox/src' folder
    for filename in glob.iglob(os.path.join(project_dir, '*.*')):
        shutil.copy(filename, SRC_DIR)

    # copy 'platformio.ini' file
    shutil.copy(project_conf, SANDBOX_DIR)

    # copy lib to '/sandbox/lib' folder
    if lib:
        shutil.copytree(lib, os.path.join(LIB_DIR, os.path.basename(lib)))

    log.info('Init finished')

    r = execute('platformio run --target upload --upload-port {}'.format(upload_port),
                directory=SANDBOX_DIR,
                capture=True)
    #log.info(r)

    with open(UPLOAD_SKIP, 'w') as f:
        f.write('1')

    log.info('Upload finished\n=========\nSTART TESTING\n=========\n')


@pytest.fixture()
def ssid(pytestconfig):
    return pytestconfig.getoption("ssid")


@pytest.fixture()
def channel(pytestconfig):
    return pytestconfig.getoption("channel")

