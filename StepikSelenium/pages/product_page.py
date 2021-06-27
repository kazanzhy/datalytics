from selenium.webdriver.common.by import By
from .base_page import BasePage
from .locators import ProductPageLocators


class ProductPage(BasePage):

    def should_be_success_message(self):
        return self.is_element_present(*ProductPageLocators.SUCCESS_MESSAGE)

    def should_not_be_success_message(self):
        assert self.is_not_element_present(*ProductPageLocators.SUCCESS_MESSAGE), "Success message is presented, but should not be"

    def success_message_should_disappeared(self):
        assert self.is_disappeared(*ProductPageLocators.SUCCESS_MESSAGE), "Success message should be disappeared, but it presented"

    def add_item_to_basket(self):
        add_button = self.browser.find_element(*ProductPageLocators.ADD_TO_BASKET_BUTTON)
        add_button.click()

    def is_product_name_in_alert(self):
        product_name = self.browser.find_element(*ProductPageLocators.PRODUCT_NAME)
        success_alert = self.browser.find_element(*ProductPageLocators.SUCCESS_ALERT)
        return product_name.text == success_alert.text

    def is_product_price_in_alert(self):
        product_price = self.browser.find_element(*ProductPageLocators.PRODUCT_PRICE)
        success_alert_price = self.browser.find_element(*ProductPageLocators.SUCCESS_ALERT_PRICE)
        return product_price.text == success_alert_price.text
