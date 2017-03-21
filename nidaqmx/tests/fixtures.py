import pytest
import nidaqmx.system
from nidaqmx.constants import ProductCategory, UsageTypeAI


class Error(Exception):
    pass


class NoFixtureDetectedError(Error):
    pass


@pytest.fixture(scope="module")
def x_series_device():
    system = nidaqmx.system.System.local()

    for device in system.devices:
        if (not device.dev_is_simulated and
                device.product_category == ProductCategory.X_SERIES_DAQ and
                len(device.ao_physical_chans) >= 2 and
                len(device.ai_physical_chans) >= 4 and
                len(device.do_lines) >= 8 and
                (len(device.di_lines) == len(device.do_lines)) and
                len(device.ci_physical_chans) >= 4):
            return device

    raise NoFixtureDetectedError(
        'Could not detect a device that meets the requirements to be an '
        'X Series fixture. Cannot proceed to run tests.')


@pytest.fixture(scope="module")
def bridge_device():
    system = nidaqmx.system.System.local()

    for device in system.devices:
        if UsageTypeAI.BRIDGE in device.ai_meas_types:
            return device

    return None
