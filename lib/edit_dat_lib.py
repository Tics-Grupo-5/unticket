from selenium.webdriver.common.by import By
import time

def open_edit_program_modal(driver, program):
    try:
        row = driver.find_element(By.XPATH, f"//td[text()='{program}']/ancestor::tr")
        button = row.find_elements(By.TAG_NAME, 'button')[0]      
        button.click()
    except:
        raise Exception(f'Program {program} not found')
    
def open_delete_program_modal(driver, program):
    try:
        row = driver.find_element(By.XPATH, f"//td[text()='{program}']/ancestor::tr")
        button = row.find_elements(By.TAG_NAME, 'button')[1]      
        button.click()
    except:
        raise Exception(f'Program {program} not found')

def UAC_check_if_program_was_added(driver, program):
    see_all_programs(driver)
    table = driver.find_element(By.XPATH, f"//div[@class='v-data-table__wrapper']//table//tbody")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        if tds[0].text == program:
            return (True, f'program {program} was added')
    return (False, f'program {program} was not added')

def UAC_check_if_program_was_deleted(driver, program):
    see_all_programs(driver)
    table = driver.find_element(By.XPATH, f"//div[@class='v-data-table__wrapper']//table//tbody")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        if tds[0].text == program:
            return (False, f'program {program} was not deleted')
    return (True, f'program {program} was deleted')

def UAC_check_if_program_was_edited(driver, program_data):
    see_all_programs(driver)
    program_data = ['' if x == None else x for x in program_data]
    table = driver.find_element(By.XPATH, f"//div[@class='v-data-table__wrapper']//table//tbody")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        data = [td.text for td in tds[:3]]
        if data == program_data:
            return (True, f'program {program_data} was edited')
    return (False, f'program {program_data} was not edited')

def see_all_programs(driver):
    select_elem = driver.find_element(By.XPATH, "//div[@class='v-data-footer__select']//div[@class='v-select__slot']")
    select_elem.click()
    time.sleep(2)
    # Locate the desired value and click on it
    value = driver.find_element(By.XPATH, f"//div[contains(@class, 'menuable__content__active')]//div[contains(text(),'All')]")
    value.click()

def get_all_programs(driver):
    see_all_programs(driver)
    table = driver.find_element(By.XPATH, f"//div[@class='v-data-table__wrapper']//table//tbody")
    rows = table.find_elements(By.TAG_NAME, 'tr')
    programs = []
    for row in rows:
        tds = row.find_elements(By.TAG_NAME, 'td')
        programs.append(tds[0].text)
    return programs