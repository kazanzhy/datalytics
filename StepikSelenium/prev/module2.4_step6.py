from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

import time 
import re
import math

def calc(x):
  return str(math.log(abs(12*math.sin(int(x)))))


link = "http://suninjuly.github.io/explicit_wait2.html"

try:
    browser = webdriver.Chrome()
    browser.get(link)

    price = WebDriverWait(browser, 12).until(EC.text_to_be_present_in_element((By.ID, "price"), '100'))


    button = browser.find_element_by_xpath("//button[text()='Book']")
    button.click()

    x_element = browser.find_element_by_id('input_value')
    x = x_element.text
    y = calc(x)

    inp = browser.find_element_by_id('answer')
    inp.send_keys(y)

    button = browser.find_element_by_xpath("//button[text()='Submit']")
    button.click()


    print(browser.switch_to.alert.text)

finally:
    # успеваем скопировать код за 30 секунд
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()

# не забываем оставить пустую строку в конце файла


