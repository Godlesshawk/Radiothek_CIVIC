import pytest
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

search_query = "Nachmittag"

@pytest.fixture( scope = "module" )
def chrome_driver():
    # Catch the Chrome Browser in variable "driver"
    driver = webdriver.Chrome( service = Service( ChromeDriverManager().install() ) )
    # Navigate Browser to given URL
    url = 'https://radiothek.orf.at/search'
    driver.get( url )

    expectation = EC.presence_of_element_located( ( By.CSS_SELECTOR, '#didomi-notice-agree-button' ) )
    cookie_accept_btn = WebDriverWait( driver, 5 ).until( expectation )
    cookie_accept_btn.click()
    time.sleep( 1 )

    yield driver

    driver.quit()


def test_1(chrome_driver):
    search_input = chrome_driver.find_element( By.CSS_SELECTOR, 'input[type=search]' )
    search_input_btn = chrome_driver.find_element( By.CSS_SELECTOR, 'button[type=submit]' )

    search_input.send_keys( search_query )
    search_input_btn.click()

    result_is_present = EC.presence_of_element_located( ( By.CSS_SELECTOR, '.search-has-query h2' ) )
    result_h2_element = WebDriverWait( chrome_driver, 5 ).until( result_is_present )
    assert result_h2_element.text == f'Suchergebnis für "{ search_query }"'

def test_2( chrome_driver ):
    all_results = chrome_driver.find_elements( By.XPATH, '//span[@class="type"]' )
    dict_results = {}
    for e in all_results:
        if e.text in dict_results:
            dict_results[e.text] += 1
        else:
            dict_results[e.text] = 1    
    assert len( dict_results ) >= 1

def test_3( chrome_driver ):
    search_option = chrome_driver.find_element( By.CSS_SELECTOR, 'span[title="Alle Sender"]' )
    search_option.click()
    result_is_present = EC.presence_of_element_located( ( By.CSS_SELECTOR, 'li[value=vbg]' ) )
    search_location = WebDriverWait( chrome_driver, 10 ).until( result_is_present )
    search_location.location_once_scrolled_into_view
    time.sleep( 2 )
    search_location.click()
    time.sleep( 2 ) # Bildschirmauflösung! Rechner zu schnell!

    new_result_is_present = EC.presence_of_all_elements_located( ( By.XPATH, '//span[@class="type"]' ) )
    new_result = WebDriverWait( chrome_driver, 10 ).until( new_result_is_present )
    dict_new_result = {}
    for i in new_result:
        if i.text in dict_new_result:
            dict_new_result[i.text] += 1
        else:
            dict_new_result[i.text] = 1
    assert len(dict_new_result) == 1
