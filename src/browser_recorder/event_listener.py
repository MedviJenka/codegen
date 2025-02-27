JS_SCRIPT = """
window.recordedInteractions = [];

// Helper function to check if an interaction already exists
function isDuplicateInteraction(newInteraction) {
    return window.recordedInteractions.some((existing) => 
        existing.action === newInteraction.action &&
        existing.xpath === newInteraction.xpath &&
        existing.value === newInteraction.value
    );
}

// Debounce utility to delay logging until typing is finished
function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

// Capture click events (no duplicates)
document.addEventListener("click", (event) => {
    const target = event.target;

    // Ignore checkboxes (they are handled separately in 'change' event)
    if (target.tagName.toLowerCase() === "input" && target.type === "checkbox") return;

    const interaction = {
        action: "click",
        tag_name: target.textContent.trim() || target.id || target.tagName.toLowerCase(),
        id: target.id || null,
        name: target.name || null,
        xpath: generateXPath(target),
        action_description: `Clicked on ${target.textContent.trim() || target.tagName.toLowerCase()}`,
        value: null
    };

    if (!isDuplicateInteraction(interaction)) {
        window.recordedInteractions.push(interaction);
    }
}, true);

// Capture input events (debounced to capture full text input)
document.addEventListener("input", debounce((event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) return;

    const interaction = {
        action: "input",
        tag_name: target.id || target.name || target.tagName.toLowerCase(),
        id: target.id || null,
        name: target.name || null,
        type: target.type.toLowerCase(),
        xpath: generateXPath(target),
        action_description: `Typed in ${target.type} field`,
        value: target.value.trim() || "" // Avoid 'None' values
    };

    if (!isDuplicateInteraction(interaction)) {
        window.recordedInteractions.push(interaction);
    }
}, 300));

// Capture final input when the user leaves the field (ensures complete text capture)
document.addEventListener("blur", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLInputElement || target instanceof HTMLTextAreaElement)) return;

    const interaction = {
        action: "input_final",
        tag_name: target.id || target.name || target.tagName.toLowerCase(),
        id: target.id || null,
        name: target.name || null,
        xpath: generateXPath(target),
        action_description: `Finished typing in ${target.type} field`,
        value: target.value.trim() || ""
    };

    if (!isDuplicateInteraction(interaction)) {
        window.recordedInteractions.push(interaction);
    }
}, true);

// Capture checkbox changes (no duplicates)
document.addEventListener("change", (event) => {
    const target = event.target;
    if (target.tagName.toLowerCase() === "input" && target.type === "checkbox") {
        const interaction = {
            action: "change",
            tag_name: target.id || target.name || `checkbox_${Date.now()}`,
            id: target.id || null,
            name: target.name || null,
            xpath: generateXPath(target),
            action_description: `Checkbox ${target.checked ? "checked" : "unchecked"}`,
            value: target.checked ? "on" : "off"
        };

        if (!isDuplicateInteraction(interaction)) {
            window.recordedInteractions.push(interaction);
        }
    }
});

// Generate XPath for elements
function generateXPath(element) {
    if (element.id) return `//*[@id="${element.id}"]`;
    if (element === document.body) return "/html/body";
    let ix = 0;
    const siblings = element.parentNode ? element.parentNode.childNodes : [];
    for (let i = 0; i < siblings.length; i++) {
        const sibling = siblings[i];
        if (sibling === element) {
            return `${generateXPath(element.parentNode)}/${element.tagName.toLowerCase()}[${ix + 1}]`;
        }
        if (sibling.nodeType === 1 && sibling.tagName === element.tagName) ix++;
    }
    return "";
}

// MutationObserver to detect dynamically added elements (ensures event listeners work on new elements)
const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
        mutation.addedNodes.forEach(node => {
            if (node.nodeType === 1 && node.matches("input, textarea, button, a")) {
                console.log("New interactable element detected:", node);
            }
        });
    }
});
observer.observe(document.body, { childList: true, subtree: true });

console.log("Event recording script initialized.");

"""
