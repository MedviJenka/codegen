JS_SCRIPT ="""
window.recordedInteractions = [];

// Debounce utility to delay logging until typing is finished
function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

// Capture click events
document.addEventListener('click', (event) => {
    const target = event.target;

    // Skip logging click events for checkboxes
    if (target.tagName.toLowerCase() === 'input' && target.type === 'checkbox') {
        return;
    }

    const tag_name = target.tagName.toLowerCase();
    const element_text = target.textContent.trim();
    const element_id = target.id.toLowerCase();
    const element_name = target.name.toLowerCase();

    const interaction = {
        action: 'click',
        tag_name: element_text || element_id || tag_name,
        id: target.id || null,
        name: target.name || null,
        xpath: generateXPath(target),
        action_description: `Clicked on ${element_text || tag_name}`,
        value: null // No value for clicks
    };
    
    window.recordedInteractions.push(interaction);

    // Detect calendar dropdown after clicking date field
    if (target.matches('input[type="text"], input.datepicker, .date-picker-field')) {
        setTimeout(() => {
            let calendar = document.querySelector('.calendar-dropdown, .datepicker-popup, [role="dialog"]');
            if (calendar) {
                console.log("Calendar dropdown detected:", calendar);
            } else {
                console.warn("Calendar dropdown not found.");
            }
        }, 500); // Small delay to allow rendering
    }
});

// Capture input events with debouncing
document.addEventListener('input', debounce((event) => {
    const target = event.target;
    const tag_name = target.tagName.toLowerCase();
    const element_id = target.id ? target.id.toLowerCase() : 'undetected';
    const element_name = target.name ? target.name.toLowerCase() : 'undetected';

    if (target.tagName.toLowerCase() === 'input' || target.tagName.toLowerCase() === 'textarea') {
        const interaction = {
            action: 'input',
            tag_name: `${element_id || tag_name}_input`,
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Typed in ${target.tagName.toLowerCase()}`,
            value: target.value || ''
        };
        window.recordedInteractions.push(interaction);
    }
}, 100));

// Checkbox handler
document.addEventListener('change', (event) => {
    const target = event.target;
    const tag = target.tagName.toLowerCase();
    const id = target.id ? target.id.toLowerCase() : null;
    const name = target.name ? target.name.toLowerCase() : null;

    if (tag === 'input' && target.type === 'checkbox') {
        const interaction = {
            action: 'change',
            tag_name: id || name || `checkbox_${Date.now()}`,
            id: id || null,
            name: name || null,
            xpath: generateXPath(target),
            action_description: `Checkbox ${target.checked ? 'checked' : 'unchecked'}`,
            value: target.checked ? 'on' : 'off'
        };
        window.recordedInteractions.push(interaction);
    }
});

// Generate XPath for an element
function generateXPath(element) {
    if (element.id) return `//*[@id="${element.id}"]`;
    if (element === document.body) return '/html/body';
    let ix = 0;
    const siblings = element.parentNode ? element.parentNode.childNodes : [];
    for (let i = 0; i < siblings.length; i++) {
        const sibling = siblings[i];
        if (sibling === element) {
            return `${generateXPath(element.parentNode)}/${element.tagName.toLowerCase()}[${ix + 1}]`;
        }
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
    }
    return '';
}

// MutationObserver to detect dynamically added elements (like calendar dropdown)
const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.matches('.calendar-dropdown, .datepicker-popup, [role="dialog"]')) {
                console.log("Calendar dynamically detected:", node);
            }
        });
    }
});
observer.observe(document.body, { childList: true, subtree: true });

// Detect calendar dropdown inside iframes
setInterval(() => {
    document.querySelectorAll('iframe').forEach(frame => {
        try {
            const frameDoc = frame.contentDocument || frame.contentWindow.document;
            const calendar = frameDoc.querySelector('.calendar-dropdown, .datepicker-popup, [role="dialog"]');
            if (calendar) {
                console.log("Calendar dropdown found inside iframe:", calendar);
            }
        } catch (error) {
            console.warn("Cross-origin iframe detected, unable to access.");
        }
    });
}, 100); // Runs periodically in case the calendar appears dynamically

"""

IMPORT_ST_DEVICE = "from qasharedinfra.devices.audc.smarttap.smarttap import SmartTap"
IMPORT_MI_DEVICE = "from qasharedinfra.devices.audc.meetinginsights.meetinginsights import MeetingInsightsSaaS"


def init_code(device: str) -> str:

    CODE = f"""
import pytest
{IMPORT_ST_DEVICE if device == 'st' else IMPORT_MI_DEVICE}
import coreinfra.core.environment.environment_variables as env
from coreinfra.services.selenium.mappedselenium import MappedSelenium
from coreinfra.services.selenium.seleniumwebelement import Actions

from qasharedinfra.infra.smarttap.selenium.utils.bini_utils import IRBiniUtils

HEADLESS = False
{device}: {'SmartTap' if device == 'st' else 'MeetingInsightsSaaS'} = env.devices['Device_1']
log = env.logger


@pytest.fixture(scope='module', autouse=True)
def init_globals() -> None:

    {device}.logger_.info('\n******** Module (Script) Setup ********')
    bini = IRBiniUtils()
    {device}.test_prerequisites(selenium=True, headless=HEADLESS)
    {device}.ui.utils.st_selenium_go_to_screen_in_current_window({device}.selenium, {device}.st_screens)  # add screen

    yield bini

    {device}.logger.info('******** Module (Script) TearDown ********')
    {device}.selenium.finalize()


@pytest.fixture(scope='function', autouse=True)
def setup_and_teardown() -> None:
    {device}.logger_.info('******** Test Setup ********')

    yield

    {device}.logger_.info('******** Test TearDown ********')

@pytest.fixture
def driver() -> MappedSelenium:
    return {device}.selenium
    
    """

    return CODE
