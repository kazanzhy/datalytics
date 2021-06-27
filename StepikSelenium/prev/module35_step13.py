from selenium import webdriver
import time
import unittest

class RegistrationTest(unittest.TestCase):
    def test_registration_1(self):
        try: 
            link = "http://suninjuly.github.io/registration1.html"
            browser = webdriver.Chrome()
            browser.get(link)

            # Ваш код, который заполняет обязательные поля
            first_name = browser.find_element_by_css_selector("input[required].form-control.first")
            first_name.send_keys("Jack")
            last_name = browser.find_element_by_css_selector("input[required].form-control.second")
            last_name.send_keys("Sparrow")
            email = browser.find_element_by_css_selector("input[required].form-control.third")
            email.send_keys("captain@blackpearl.com")
            # Отправляем заполненную форму
            button = browser.find_element_by_css_selector("button.btn")
            button.click()
            # Проверяем, что смогли зарегистрироваться
            # ждем загрузки страницы
            time.sleep(1)
            # находим элемент, содержащий текст
            welcome_text_elt = browser.find_element_by_tag_name("h1")
            # записываем в переменную welcome_text текст из элемента welcome_text_elt
            welcome_text = welcome_text_elt.text
            # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
            assert welcome_text == "Congratulations! You have successfully registered!"
        finally:
            # ожидание чтобы визуально оценить результаты прохождения скрипта
            time.sleep(10)
            # закрываем браузер после всех манипуляций
            browser.quit()

    def test_registration_2(self):
        try: 
            link = "http://suninjuly.github.io/registration2.html"
            browser = webdriver.Chrome()
            browser.get(link)
            # Ваш код, который заполняет обязательные поля
            first_name = browser.find_element_by_css_selector("input[required].form-control.first")
            first_name.send_keys("Jack")
            last_name = browser.find_element_by_css_selector("input[required].form-control.second")
            last_name.send_keys("Sparrow")
            email = browser.find_element_by_css_selector("input[required].form-control.third")
            email.send_keys("captain@blackpearl.com")
            # Отправляем заполненную форму
            button = browser.find_element_by_css_selector("button.btn")
            button.click()
            # Проверяем, что смогли зарегистрироваться
            # ждем загрузки страницы
            time.sleep(1)
            # находим элемент, содержащий текст
            welcome_text_elt = browser.find_element_by_tag_name("h1")
            # записываем в переменную welcome_text текст из элемента welcome_text_elt
            welcome_text = welcome_text_elt.text
            # с помощью assert проверяем, что ожидаемый текст совпадает с текстом на странице сайта
            assert welcome_text == "Congratulations! You have successfully registered!"
        finally:
            # ожидание чтобы визуально оценить результаты прохождения скрипта
            time.sleep(10)
            # закрываем браузер после всех манипуляций
            browser.quit()

if __name__ == "__main__":
    unittest.main()

