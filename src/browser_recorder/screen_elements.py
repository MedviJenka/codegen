import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

PAGE_BASE = "elements_data.csv"  # Define your CSV file

def get_element_xpath(driver, element):
    """Generate an XPath for an element."""
    return driver.execute_script("""
        function getElementXPath(elt) {
            var path = "";
            for (; elt && elt.nodeType == 1; elt = elt.parentNode) {
                idx = 1;
                for (var sib = elt.previousSibling; sib; sib = sib.previousSibling) {
                    if (sib.nodeType == 1 && sib.tagName == elt.tagName) idx++;
                }
                xname = elt.tagName.toLowerCase();
                xname += "[" + idx + "]";
                path = "/" + xname + path;
            }
            return path;
        }
        return getElementXPath(arguments[0]);
    """, element)

def extract_and_sort_elements(driver):
    """Extract elements and sort by ID, then Name, then XPath."""
    elements_data = []
    elements = driver.find_elements(By.XPATH, "//*")  # Get all elements

    for elem in elements:
        elem_id = elem.get_attribute("id")
        elem_name = elem.get_attribute("name")
        elem_type = elem.tag_name  # Element Type (button, input, div, etc.)
        elem_xpath = get_element_xpath(driver, elem)
        elem_action = "click" if elem.tag_name in ["button", "a"] else "input"  # Determine action
        elem_value = elem.get_attribute("value") or ""

        # Sorting priority: ID > Name > XPath
        identifier = elem_id if elem_id else elem_name if elem_name else elem_xpath

        elements_data.append({
            "Element Name": identifier,
            "Element Type": elem_type,
            "Element Path": elem_xpath,
            "Action": elem_action,
            "Value": elem_value
        })

    # Sort elements: ID > Name > XPath
    elements_data.sort(key=lambda x: (x["Element Name"] != x["Element Path"], x["Element Name"]))

    return elements_data

def save_to_csv(elements_data):
    """Save elements to CSV file."""
    with open(PAGE_BASE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Element Name", "Element Type", "Element Path", "Action", "Value"])
        for elem in elements_data:
            writer.writerow([elem["Element Name"], elem["Element Type"], elem["Element Path"], elem["Action"], elem["Value"]])

def run_scraper():
    """Run the Selenium scraper and extract elements."""
    driver = webdriver.Chrome()  # Use appropriate driver
    driver.get("https://www.google.com")  # Replace with target URL

    elements = extract_and_sort_elements(driver)
    save_to_csv(elements)

    driver.quit()
    print(f"Extracted {len(elements)} elements and saved to {PAGE_BASE}")

if __name__ == "__main__":
    run_scraper()
