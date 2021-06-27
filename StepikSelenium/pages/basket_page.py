from selenium.webdriver.common.by import By
from .base_page import BasePage
from .locators import BasketPageLocators


class BasketPage(BasePage):

    def basket_should_be_empty(self):
        assert self.is_element_present(*BasketPageLocators.BASKET_EMPTY), "Basket is not empty"

    def basket_should_contain_empty_text(self):
        basket_container = self.browser.find_element(*BasketPageLocators.BASKET_EMPTY)
        print(basket_container.text)
        assert 'Your basket is empty' in basket_container.text, "There is no text says than basket is empty"
