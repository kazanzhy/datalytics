from selenium import webdriver
import time
import unittest
import time
import math

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

result = []
@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()

@pytest.mark.parametrize('lesson', ['236895','236896','236897','236898','236899','236903','236904','236905'])
def test_hidden_message(browser, lesson):
    global result
    link = f'https://stepik.org/lesson/{lesson}/step/1'
    browser.get(link)
    inp = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea.ember-text-area.ember-view")))
    answer = math.log(int(time.time()))
    inp.send_keys(str(answer))
    button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME , "submit-submission")))
    button.click()
    feedback = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "smart-hints__hint")))
    assert feedback.text == 'Correct!', feedback.text
 



#The owls are not what they seem! OvO
