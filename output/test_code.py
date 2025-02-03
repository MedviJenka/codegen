
        
import pytest
from qasharedinfra.devices.audc.smarttap.smarttap import SmartTap
import coreinfra.core.environment.environment_variables as env
from coreinfra.services.selenium.mappedselenium import MappedSelenium
from coreinfra.services.selenium.seleniumwebelement import Actions

from qasharedinfra.infra.smarttap.selenium.utils.bini_utils import IRBiniUtils

HEADLESS = False
st: SmartTap = env.devices['Device_1']
log = env.logger


@pytest.fixture(scope='module', autouse=True)
def init_globals() -> None:

    st.logger_.info('
******** Module (Script) Setup ********')
    bini = IRBiniUtils()
    st.test_prerequisites(selenium=True, headless=HEADLESS)
    st.ui.utils.st_selenium_go_to_screen_in_current_window(st.selenium, st.st_screens)  # add screen

    yield bini

    st.logger.info('******** Module (Script) TearDown ********')
    st.selenium.finalize()


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown() -> None:
    st.logger_.info('******** Test Setup ********')

    yield

    st.logger_.info('******** Test TearDown ********')

@pytest.fixture
def driver() -> MappedSelenium:
    return st.selenium
    
    
        class TestNone:

            def test_None(self, driver) -> None:
                driver.get_mapped_element('Sign in with Microsoft 365').action(Actions.CLICK)
driver.get_mapped_element('i0116_input').inject_text('qa_auto_user_1@ai-logix.net')
driver.get_mapped_element('idsibutton9').action(Actions.CLICK)
driver.get_mapped_element('i0118_input').inject_text('S')
driver.get_mapped_element('undetected_input').inject_text('on')
driver.get_mapped_element('undetected_input').inject_text('on')
driver.get_mapped_element('undetected_input').inject_text('on')
driver.get_mapped_element('Action').action(Actions.CLICK)
driver.get_mapped_element('Export to Excel').action(Actions.CLICK)
driver.get_mapped_element('export').action(Actions.CLICK)
driver.get_mapped_element('a').action(Actions.CLICK)
driver.get_mapped_element('daterange-header-filter').action(Actions.CLICK)
driver.get_mapped_element('Current Month').action(Actions.CLICK)
driver.get_mapped_element('8').action(Actions.CLICK)
driver.get_mapped_element('Apply').action(Actions.CLICK)
        