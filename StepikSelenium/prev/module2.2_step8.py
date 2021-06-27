from selenium import webdriver
import time

try: 
    link = "http://suninjuly.github.io/file_input.html"
    browser = webdriver.Chrome()
    browser.get(link)

    # Ваш код, который заполняет обязательные поля
    first_name = browser.find_element_by_name("firstname")
    first_name.send_keys("Jack")
    last_name = browser.find_element_by_name("lastname")
    last_name.send_keys("Sparrow")
    email = browser.find_element_by_name("email")
    email.send_keys("captain@blackpearl.com")

    f = browser.find_element_by_id('file')
    f.send_keys("/home/sirius/Text.txt")

    # Отправляем заполненную форму
    button = browser.find_element_by_css_selector("button.btn")
    button.click()

    print(browser.switch_to.alert.text)

    # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()
#
