import pytest
import integration

@pytest.fixture(scope='session')
def xctrl():
    xctrl = integration.xcontrol()
    yield xctrl
    try:
        xctrl.proc.terminate()
    except:
        pass
