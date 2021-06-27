from .base_page import BasePage
from .locators import LoginPageLocators
import time

class LoginPage(BasePage):

    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url

    def should_be_login_page(self):
        self.should_be_login_url()
        self.should_be_login_form()
        self.should_be_register_form()

    def should_be_login_url(self):
        assert 'login' in self.browser.current_url, "Word 'login' is not in LoginPage URL"

    def should_be_login_form(self):
        assert self.is_element_present(*LoginPageLocators.LOGIN_FORM), "Login form is not presented in LoginPage"

    def should_be_register_form(self):
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "Registration form is not presented in LoginPage"

    def register_new_user(self, email, password):
        
        assert self.is_element_present(*LoginPageLocators.REGISTER_FORM), "There is not Register form"

        email_input = self.browser.find_element(*LoginPageLocators.REGISTER_EMAIL)
        email_input.send_keys(email)

        pass1_input = self.browser.find_element(*LoginPageLocators.REGISTER_PASSWORD1)
        pass1_input.send_keys(password)

        pass2_input = self.browser.find_element(*LoginPageLocators.REGISTER_PASSWORD2)
        pass2_input.send_keys(password)

        button = self.browser.find_element(*LoginPageLocators.REGISTER_BUTTON)
        button.click()
