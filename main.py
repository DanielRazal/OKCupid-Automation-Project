from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from translate import Translator
from datetime import datetime
import pytz


def webDriverWait(driver, by, xpath, timeout=10):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.presence_of_element_located((by, xpath)))
    return element

def save_cookies(driver, path):
    with open(path, 'w') as file:
        json.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    with open(path, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

def read_json_file(path):
    with open(path, 'r') as file:
        return json.load(file)

    
def test_login(driver):
    
    okCupid = read_json_file('okCupid.json')
    
    email_key = okCupid['email']['name']
    password_key = okCupid['password']['name']
    next_button_xpath = okCupid['next_button']['xpath']
    send_code_button_xpath = okCupid['send_code_button']['xpath']
    
    sign_in_button = webDriverWait(driver,By.LINK_TEXT,'Sign in')
    sign_in_button.click()
    
    email = webDriverWait(driver,By.ID,'username')
    email.send_keys(email_key)
    
    password = webDriverWait(driver,By.ID,'password')
    password.send_keys(password_key)
    
    next_button = webDriverWait(driver,By.XPATH,next_button_xpath)
    next_button.click()
    
    time.sleep(2)
    
    send_code_button = webDriverWait(driver,By.XPATH,send_code_button_xpath)
    send_code_button.click()
    
    # Manually write the code you received on the phone

    time.sleep(20)
    
    save_cookies(driver, "okCupid_cookies.json")
    
def change_text_by_time(driver,send_message_text,translation):
    israel_tz = pytz.timezone('Asia/Jerusalem')
    israel_time = datetime.now(israel_tz)
    
    if 5 <= israel_time.hour < 12:
        ActionChains(driver).move_to_element(send_message_text).click().send_keys(f"היי {translation} בוקר טוב, אשמח להכיר 🌹").perform()
    elif 12 <= israel_time.hour < 17:
        ActionChains(driver).move_to_element(send_message_text).click().send_keys(f"היי {translation} צהריים טוב, אשמח להכיר 🌹").perform()
    elif 17 <= israel_time.hour < 24:
        ActionChains(driver).move_to_element(send_message_text).click().send_keys(f"היי {translation} ערב טוב, אשמח להכיר 🌹").perform()
    elif 1 <= israel_time.hour < 5:
        ActionChains(driver).move_to_element(send_message_text).click().send_keys(f"היי {translation} לילה טוב, אשמח להכיר 🌹").perform()
    else:
        ActionChains(driver).move_to_element(send_message_text).click().send_keys(f"היי {translation} בוקר טוב, אשמח להכיר 🌹").perform()


def translate_name_for_hebrew(driver):
    element = driver.find_element(By.CSS_SELECTOR, ".card-content-header__text")
    text = element.text
    translator = Translator(to_lang='he')
    translation = translator.translate(text)
    return translation


def test_send_messages_to_users(driver):
    okCupid = read_json_file('okCupid.json')
    
    intro_button_xpath = okCupid['intro_button']['xpath']
    send_message_button_xpath = okCupid['send_message_button']['xpath']
    keep_browsing_button_xpath = okCupid['keep_browsing_button']['xpath']
    send_message_button_id = "messenger-composer"
    for i in range(200):
        
        intro_button = webDriverWait(driver, By.XPATH, intro_button_xpath)
        if intro_button:
            try:
                intro_button.click()
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(e)

        time.sleep(3)
        send_message_text = webDriverWait(driver, By.ID, send_message_button_id)
        if send_message_text:
            
            translation = translate_name_for_hebrew(driver)
            time.sleep(5)
            change_text_by_time(driver,send_message_text,translation)
            time.sleep(2)

        send_message_button = webDriverWait(driver, By.XPATH, send_message_button_xpath)
        if send_message_button:
            try:
                send_message_button.click()
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(e)

        time.sleep(3)

        keep_browsing_button = webDriverWait(driver, By.XPATH, keep_browsing_button_xpath)
        if keep_browsing_button:
            try:
                keep_browsing_button.click()
            except (StaleElementReferenceException, NoSuchElementException) as e:
                print(e)

        time.sleep(8)

        print(i)
    
    
if __name__ == '__main__':
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://www.okcupid.com/home')
    driver.maximize_window()
    # test_login(driver)
    load_cookies(driver, "okCupid_cookies.json")
    driver.refresh()
    time.sleep(5)
    test_send_messages_to_users(driver)
    time.sleep(10)
    driver.quit()