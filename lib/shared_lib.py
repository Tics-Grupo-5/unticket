import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils.urls import URLs
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import utils.months as months
import re

def init_driver():
    # Create a new instance of the Chrome driv
    options = webdriver.ChromeOptions()
    options.add_argument('--log-level=3') # set log level to SEVERE
    options.add_experimental_option("prefs", {
        "download.default_directory": os.path.abspath(r'downloads'),
    })
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def go_to_url(driver, urlkey):
    url = URLs[urlkey]
    # Go to the URL
    driver.get(url)

def switch_to_window(driver, idx):
    # Switch to the new window
    driver.switch_to.window(driver.window_handles[idx])

def quit_driver(driver):
    # Close the browser window
    driver.quit()

def UAC_check_current_url(driver, urlkey):
    url = URLs[urlkey]
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.url_to_be(url))
        if driver.current_url == url:
            return (True, f'{urlkey} reached')
        else:
            return (False, f'{urlkey} not reached')
    except Exception:
        return (False, f'{urlkey} not reached')
    
def UAC_check_redirection(driver, urlkey1, urlkey2):
    url1 = URLs[urlkey1]
    url2 = URLs[urlkey2]
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.url_to_be(url2))
        if driver.current_url == url2:
            return (True, f'successful redirection from {urlkey1} to {urlkey2}')
        else:
            return (False, f'failed redirection from {urlkey1} to {urlkey2}')
    except Exception:
        return (False, f'failed redirection from {urlkey1} to {urlkey2}')
    
def select_role(driver, role):
    # Click on the dropdown list
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='v-select__selections']")))
    dropdown.click()
    # Locate the desired value and click on it
    value = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{role}')]")))
    value.click()

def get_role(driver):
    # Click on the dropdown list
    dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='v-select__selections']")))
    return dropdown.text

def evaluate_UAC_result(result):
    if result[0] == True:
        print('UAC PASSED:', result[1])
        return 1
    else:
        print('UAC FAILED:', result[1])
        return 0
    
def evaluate_composite_UAC_result(results):
    for result in results:
        if result[0] != True:
            print('UAC Failed:', result[1])
            return 0
    print('UAC PASSED:', [result[1] for result in results])
    return 1
    
def select_module(driver, module):
    # find the element by the link text "Ver certificados"
    element = driver.find_element(By.XPATH, f"//div[text()='{module}']/ancestor::a")

    # click the element
    element.click()

def click_button(driver, text, idx=0):
    # find the element by the link text "Ver certificados"
    element = driver.find_elements(By.XPATH, f"//span[contains(text(),'{text}')]/ancestor::button")[idx]

    # click the element
    element.click()

def click_link(driver, text, idx=0):
    # find the element by the link text "Ver certificados"
    element = driver.find_elements(By.XPATH, f"//span[contains(text(),'{text}')]/ancestor::a")[idx]

    # click the element
    element.click()

def enter_input_value(driver, label, value, mode=0):
    # Find the label element with the matching text
    label_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")

    # Find the input element next to the label
    input_element = label_element.find_element(By.XPATH, "./following-sibling::input")

    if mode == 0: # mode 1 is for files, for those fields, we cannot do this
        input_element.send_keys(Keys.CONTROL + "a")
        input_element.send_keys(Keys.DELETE)

    time.sleep(1)

    # Enter the desired value into the input element
    input_element.send_keys(value)

def get_input_value(driver, label):
    # Find the label element with the matching text
    label_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")

    # Find the input element next to the label
    input_element = label_element.find_element(By.XPATH, "./following-sibling::input")

    return input_element.get_attribute('value')

def get_multiselect_values(driver, label):
    # Find the label element with the matching text
    label_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")

    # Find the input element next to the label
    elements = label_element.find_elements(By.XPATH, "./following-sibling::div//span[@class='v-chip__content']")

    return [e.text for e in elements]

def enter_textarea_value(driver, label, value):
    # Find the label element with the matching text
    label_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")

    # Find the input element next to the label
    input_element = label_element.find_element(By.XPATH, "./following-sibling::textarea")

    input_element.send_keys(Keys.CONTROL + "a")
    input_element.send_keys(Keys.DELETE)

    # Enter the desired value into the input element
    input_element.send_keys(value)

def get_textarea_value(driver, label):
    # Find the label element with the matching text
    label_element = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")

    # Find the input element next to the label
    input_element = label_element.find_element(By.XPATH, "./following-sibling::textarea")

    return input_element.get_attribute('value')

def select_value(driver, label, value, strict=False):
    dropdown = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]/following-sibling::div[@class='v-select__selections']")
    dropdown.click()
    time.sleep(2)
    # Locate the desired value and click on it
    if strict: 
        value = driver.find_element(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[normalize-space()='{value}']")
        value.click()
    else:
        value = driver.find_element(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[contains(text(),'{value}')]")
        value.click()


def get_select_dropdown_values(driver, label):
    dropdown = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]/following-sibling::div[@class='v-select__selections']")
    dropdown.click()
    time.sleep(2)
    # Locate the desired value and click on it
    values = driver.find_elements(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[@class='v-list-item__title']")
    return [v.text for v in values]

def multiselect_values(driver, label, values):
    dropdown = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")
    dropdown.click()

    checkboxes = driver.find_elements(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[@class='v-simple-checkbox']")
    for checkbox in checkboxes: 
        # dot to not use absolute path
        i = checkbox.find_element(By.XPATH, './/div[@class="v-input--selection-controls__input"]/i')
        if 'mdi-checkbox-marked' in i.get_attribute('class'):
            time.sleep(0.5)
            checkbox.click()

    # Locate the desired value and click on it
    for value in values:
        checkbox = driver.find_element(By.XPATH, f"//div[text()='{value}']/ancestor::div/preceding-sibling::div[contains(@class, 'v-list-item__action')]/div[contains(@class, 'v-simple-checkbox')]")
        checkbox.click()

def get_dropdown_multiselect_values(driver, label):
    dropdown = driver.find_element(By.XPATH, f"//label[contains(text(),'{label}')]")
    dropdown.click()

    items = driver.find_elements(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[@class='v-list-item__title']")
    values = [item.text for item in items]
    return values

def click_checkbox(driver, label):
    checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]/preceding-sibling::div//input[@type='checkbox']/following-sibling::div")
    checkbox.click()

def get_checkbox_value(driver, label):
    checkbox = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]/preceding-sibling::div//input[@type='checkbox']")
    return checkbox.is_selected()

def press_esc_key(driver):
    # Create an ActionChains instance
    actions = ActionChains(driver)
    # Simulate pressing the ESC key
    actions.send_keys(Keys.ESCAPE).perform()

def search(driver, label, value):
    # Find the input field within the div element of text "text"
    input_field = driver.find_element(By.XPATH, f"//div[contains(text(), '{label}')]//input")

    input_field.send_keys(Keys.CONTROL + "a")
    input_field.send_keys(Keys.DELETE)

    # Type text into the input field
    input_field.send_keys(value)

def UAC_check_unique_record(driver, tablename, value):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), '{tablename}')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) == 1:
        return (True, f'1 record found for {value}')
    return (False, f'multiple records found for {value}')


def UAC_validate_saved_record(driver, tablename, values, idx):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), '{tablename}')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        if rows[0].text == 'No matching records found':
            return (False, f'no records found for {values}')
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        tds = tds[:len(values)]
        if len(tds) > 0:
            for td, value in zip(tds, values):
                if value == None:
                    continue
                real_value = ' '.join(sorted(td.text.lower().split())) 
                expected_value = ' '.join(sorted(value.lower().split()))
                print(real_value, expected_value)
                if real_value != expected_value:
                    return (False, f"mismatch between: [{real_value}] and {expected_value}]")
            return (True, f"record data match with [{values}]")
    return (False, f"no records found for [{', '.join(values)}]")

def click_edit_button(driver, tablename, idx, pos=1):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), '{tablename}')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        button = tds[-1].find_elements(By.TAG_NAME, 'button')[pos]
        button.click()
    else:
        raise Exception('No records found')
    
def click_eye_button(driver, tablename, idx):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), '{tablename}')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        button = tds[-1].find_elements(By.TAG_NAME, 'button')[0]
        button.click()
    else:
        raise Exception('No records found')
    

def read_cert_status(driver, idx):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), 'Certificados')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        status = tds[2].text
        return status
    else:
        raise Exception('No records found')
    

def UAC_check_search_results(driver, tablename, keyword, column, unique, expected):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), '{tablename}')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) == 1 and rows[0].text == 'No matching records found':
        if expected:
            return (False, f'no records found for {keyword}')
        return (True, f'no records found for {keyword} as expected')
    if unique:
        if len(rows) > 1:
            return (False, f'multiple records found for {keyword}')
        row = rows[0]
        tds = row.find_elements(By.TAG_NAME, 'td')
        td = tds[column]
        if keyword in td.text:
            return (True, f'one result found for {keyword}')
        return (False, f'{keyword} not found in {td.text}')
    else:
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, 'td')
            td = tds[column]
            if keyword not in td.text:
                return (False, f'{keyword} not found in {td.text}')
        return (True, f'{keyword} found in every row')
    

def set_date_field_value(driver, mode, label, date_str):

    year = date_str[:4] 
    month = months.translate_month(date_str[5:7])
    day = int(date_str[8:]) # int to remove trailing zero

    # Find the input field element
    input_elem = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]/ancestor::div[@class='v-text-field__slot']")
    # Click the input field to open the date picker
    input_elem.click()

    if mode == 0:
        input_elem.click()

    time.sleep(2)

    if mode == 1:
        year_buttons = driver.find_elements(By.XPATH, f"//div[@class='v-picker__title__btn v-date-picker-title__year']")

        # Multiple modals are created => Then, check visibility
        year_button = None
        for possible in year_buttons:
            if possible.is_displayed():
                year_button = possible
                break

        year_button.click()

    wait = WebDriverWait(driver, 10)
    year_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//li[text()='{year}']")))

    # Click the year element to select it
    year_element.click()

    month_element = wait.until(EC.visibility_of_element_located((By.XPATH, f"//div[text()='{month}']/ancestor::button")))
    month_element.click()

    time.sleep(1)

    day_elements = driver.find_elements(By.XPATH, f"//div[text()='{day}']/ancestor::button")

    # Multiple modals are create => Then, check visibility
    day_element = None
    for possible in day_elements:
        if possible.is_displayed():
            day_element = possible
            break

    day_element.click()

    if mode == 1:
        oks = driver.find_elements(By.XPATH, f"//span[contains(text(),'OK')]/ancestor::button")
        
        # Multiple modals are created => Then, check visibility
        ok = None
        for possible in oks:
            if possible.is_displayed():
                ok = possible
                break

        ok.click()
        

def descargar_soporte(driver, idx):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), 'Mis Solicitudes')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        anchor = tds[-2].find_element(By.TAG_NAME, 'a')
        anchor.click()
    else:
        raise Exception('No records found')

def descargar_soporte_from_edit_form(driver):
    link_element = driver.find_element(By.LINK_TEXT, 'Soporte de pago')
    link_element.click()

def descargar_certificado(driver, idx):
    table = driver.find_element(By.XPATH, f"//div[contains(text(), 'Mis Solicitudes')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    if len(rows) > 0:
        row = rows[idx]
        tds = row.find_elements(By.TAG_NAME, 'td')
        anchor = tds[-1].find_element(By.TAG_NAME, 'a')
        anchor.click()
    else:
        raise Exception('No records found')

def UAC_validate_downloaded_filename(file_name, file):
    folder = os.path.abspath('downloads')
    filename = max([os.path.join(folder, f) for f in os.listdir(folder)], key=os.path.getctime)
    while 'crdownload' in filename or 'tmp' in filename:
        print('waiting for download to finish ...')
        time.sleep(5)
        filename = max([os.path.join(folder, f) for f in os.listdir(folder)], key=os.path.getctime)
    basename = os.path.basename(filename)
    if file == 0:
        pattern = re.compile(r"\d{4}-\d")
        if pattern.match(basename[:6]) and basename[7:].startswith(file_name):
            return (True, f'valid filename for {file_name}: {basename}')
        return (False, f'invalid filename for {file_name}: {basename}')
    elif file == 1:
        pattern = re.compile(r"C_\d{4}-\d")
        if pattern.match(basename[:8]) and basename[9:].startswith(file_name):
            return (True, f'valid filename for {file_name}: {basename}')
        return (False, f'invalid filename for {file_name}: {basename}')
    elif file == 2 or file == 3 or file == 5:
        if basename.startswith(file_name):
            return (True, f'valid filename for {file_name}: {basename}')
        return (False, f'invalid filename for {file_name}: {basename}')
    elif file == 4:
        pattern = re.compile(r"\d{4}-\d")
        if pattern.match(basename[14:20]) and basename[:14].startswith(file_name):
            return (True, f'valid filename for {file_name}: {basename}')
        return (False, f'invalid filename for {file_name}: {basename}')


def UAC_validate_input_field(driver, targetInputFieldLabel, expectedValue):
    input = driver.find_element(By.XPATH, f"//label[text()='{targetInputFieldLabel}']/following-sibling::input")
    return (input.text == expectedValue, f'The input field with label {targetInputFieldLabel} does not match value: {expectedValue}')

def UAC_compare_form_fields(actual_values, expected_values):
    for a, b in zip(actual_values, expected_values):
        if str(a) != str(b):
            return (False, f'mismatch between {a} and {b}')
    return (True, f'all values match: {actual_values}, {expected_values}')

def UAC_check_two_lists(list1, list2):
    if sorted(list1) == sorted(list2):
        return (True, f'both lists are equal: {list1}, {list2}')
    return (False, f'lists are different: {list1}, {list2}')

def UAC_check_element_in_dropdown(element, dropdown_elements):
    if element in dropdown_elements:
        return (True, f'element {element} is in dropdown: {dropdown_elements}')
    return (False, f'element {element} is not in dropdown: {dropdown_elements}')

def UAC_check_element_not_in_dropdown(element, dropdown_elements):
    if element not in dropdown_elements:
        return (True, f'element {element} is in dropdown: {dropdown_elements}')
    return (False, f'element {element} is not in dropdown: {dropdown_elements}')

def see_all_items(driver):
    select_elem = driver.find_element(By.XPATH, "//div[@class='v-data-footer__select']//div[@class='v-select__slot']")
    select_elem.click()
    time.sleep(2)
    # Locate the desired value and click on it
    value = driver.find_element(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[contains(text(),'All')]")
    value.click()

def UAC_check_estados_for_role(estados, role):
    if role in ['Administrador', 'Gestor 1', 'Gestor 2']:
        if sorted(estados) == sorted(['Radicado', 'En trámite', 'Aclaración', 'Elaborado', 'Cerrado']):
            return (True, f'available estados are correct for role {role}')
        return (False, f'available estados are incorrect for role {role}')
    elif role == 'Recepción':
        if estados == ['Cerrado']:
            return (True, f'available estados are correct for role {role}')
        return (False, f'available estados are incorrect for role {role}')

def UAC_check_registro_de_actividad(driver, keywords):
    card = driver.find_element(By.XPATH, '(//div[contains(@class, "v-card v-sheet")])[last()]')
    for keyword in keywords:
        if keyword not in card.text:
            return (False, f'{keyword} not in registro de actividad')
    return (True, f'{keywords} in registro de actividad')

def get_all_solicitudes_ids(driver):
    see_all_items(driver)
    table = driver.find_element(By.XPATH, f"//div[contains(text(), 'Mis Solicitudes')]/following-sibling::div//table")
    tbody = table.find_element(By.TAG_NAME, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, 'tr')
    ids = []
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        ids.append(tds[0].text)
    return ids