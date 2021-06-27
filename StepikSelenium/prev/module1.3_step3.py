from selenium import webdriver
from selenium.webdriver.support.ui import Select

import time 
import re
import math




link = "http://SunInJuly.github.io/execute_script.html."

try:
    browser = webdriver.Chrome()
    browser.get(link)

    num1 = browser.find_element_by_id('num1').text
    num2 = browser.find_element_by_id('num2').text
    s = int(num1) + int(num2)

    select = Select(browser.find_element_by_id('dropdown'))
    select.select_by_value(str(s)) 

    button = browser.find_element_by_xpath("//button[text()='Submit']")
    button.click()
    print(browser.switch_to.alert.text)

finally:
    # успеваем скопировать код за 30 секунд
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()

# не забываем оставить пустую строку в конце файла


