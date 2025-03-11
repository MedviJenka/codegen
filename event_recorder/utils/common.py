TASK = """
based on code format given bellow, if the device is set to smarttap or st: all the imports should be:
from qasharedinfra.infra.<smarttap>.general_utils import get_file_size
and
st: SmartTap = env.devices['Device_1']
if the device was set to 'mi' all the imports should include meetinginsights instead of smarttap
from qasharedinfra.infra.meetinginsights.selenium.utils.custom_exceptions import ElementIsClickableException
and replace st with:
mi: MeetingInsightsSaaS = env.devices['Device_1']
"""

CODE_FORMAT = """
import pytest
import coreinfra.core.environment.environment_variables as env
from selenium.common import ElementClickInterceptedException
from coreinfra.services.selenium.mappedselenium import MappedSelenium
from coreinfra.services.selenium.seleniumwebelement import Actions
from qasharedinfra.devices.audc.smarttap.smarttap import SmartTap
from qasharedinfra.infra.smarttap.general_utils import get_file_size
from qasharedinfra.infra.common.services.ai.infrastructure.utils import BiniUtils
from qasharedinfra.infra.smarttap.selenium.utils.custom_exceptions import ElementIsClickableException
from qasharedinfra.infra.smarttap.selenium.utils.enums.interaction_page_enums import CallIconsEnum
from qasharedinfra.infra.smarttap.selenium.utils.interactions_page_utils import negative
from qasharedinfra.infra.smarttap.selenium.utils.common_utils import get_file_by_type_from_downloads_folder, hover_over_element


HEADLESS = False
st: SmartTap = env.devices['Device_1']
log = env.logger


@pytest.fixture(scope='module', autouse=True)
def init_globals() -> None:

    st.logger_.info('\n******** Module (Script) Setup ********')
    bini = BiniUtils()
    st.test_prerequisites(selenium=True, headless=HEADLESS)
    st.ui.utils.st_selenium_go_to_screen_in_current_window(st.selenium, st.st_screens.interactions)

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


class TestDownloadCall:

    @staticmethod
    def get_call_id_by_call_icon_status(driver, call_icon=CallIconsEnum.AVAILABLE_ICON) -> list:
        driver.get_mapped_element(element_name='call_icons_filter').action(Actions.CLICK)
        driver.get_mapped_element(element_name='available_icons', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='empty_screen', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='select_columns').action(Actions.CLICK)
        driver.get_mapped_element(element_name='hide_all_columns').action(Actions.CLICK)
        driver.get_mapped_element(element_name='select_columns:original_call_id').action(Actions.CLICK)

        try:
            call_id = driver.get_mapped_element(element_name='first_row_call_id').get_text()
            return call_id

        except Exception as e:
            log.error(f'there is no calls with this call status. icon: {call_icon.name},  {e}')
            raise e

    def test_download_last_available_call(self, driver, call_icon=CallIconsEnum.AVAILABLE_ICON) -> None:
        call_id = self.get_call_id_by_call_icon_status(driver, call_icon=call_icon)
        driver.get_mapped_element(element_name='filter:by_call_id').inject_text(call_id)
        driver.get_mapped_element(element_name='first_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='action_button').action(Actions.CLICK)
        driver.get_mapped_element(element_name='download_audio').action(Actions.CLICK)
        last_ogg_file = get_file_by_type_from_downloads_folder(file_type='ogg')
        assert call_id in last_ogg_file
        assert get_file_size(file_path=last_ogg_file) > 1, log.bug('')

    @negative
    def test_download_unavailable_icon(self, driver) -> None:
        try:
            self.test_download_last_available_call(driver=driver, call_icon=CallIconsEnum.UNAVAILABLE_ICON)

        except ElementClickInterceptedException as e:
            log.info(f'download button is not clickable as expected, exception: {e}')
            raise e
        with pytest.raises(Exception):
            log.error('')
            raise Exception

    @negative
    def test_download_multiple_calls(self, driver):
        call_icon = CallIconsEnum.AVAILABLE_ICON
        driver.get_mapped_element(element_name='call_icons_filter').action(Actions.CLICK)
        driver.get_mapped_element(element_name='available_icons', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='empty_screen', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='first_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='second_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='action_button').action(Actions.CLICK)

        try:
            driver.get_mapped_element(element_name='download_audio').action(Actions.CLICK)

        except ElementClickInterceptedException as e:
            raise e
        with pytest.raises(Exception):
            raise Exception

    @staticmethod
    def __test_hover_on_download_audio_button(driver) -> None:
        call_icon = CallIconsEnum.AVAILABLE_ICON
        driver.get_mapped_element(element_name='call_icons_filter').action(Actions.CLICK)
        driver.get_mapped_element(element_name='available_icons', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='empty_screen', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='first_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='second_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='action_button').action(Actions.CLICK)
        hover_over_element(device=driver, element_name='download_audio')

    @negative
    def test_meeting_call_type_cannot_be_downloaded(self, driver) -> None:

        REMARK: at this moment meeting call type cannot be downloaded

        # filter available call
        call_icon = CallIconsEnum.AVAILABLE_ICON
        driver.get_mapped_element(element_name='call_icons_filter').action(Actions.CLICK)
        driver.get_mapped_element(element_name='available_icons', index=call_icon).action(Actions.CLICK)
        driver.get_mapped_element(element_name='empty_screen', index=call_icon).action(Actions.CLICK)

        # filter meeting call type
        driver.get_mapped_element(element_name='call_type_dropdown').action(Actions.CLICK)
        driver.get_mapped_element(element_name='filter:by_call_type', index='3').action(Actions.CLICK)

        # download call
        driver.get_mapped_element(element_name='first_row_checkbox').action(Actions.CLICK)
        driver.get_mapped_element(element_name='action_button').action(Actions.CLICK)

        try:
            driver.get_mapped_element(element_name='download_audio').action(Actions.CLICK)
        except ElementIsClickableException as EICE:
            log.error(message=f"Exception caught: {EICE}")
            pass
"""
