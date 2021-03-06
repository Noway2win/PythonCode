from selenium.webdriver.common.by import By

from .abstract import PageElement
from .abstract import PageObject

class HelloPage(PageObject):
    button_greet = PageElement(By.CSS_SELECTOR, "button#greet-button-id")
    button_reset = PageElement(By.CSS_SELECTOR, "button#reset")
    input_name = PageElement(By.CSS_SELECTOR, "input#xxx-id")
    input_surname = PageElement(By.CSS_SELECTOR, "input#surname-id")
    input_age = PageElement(By.CSS_SELECTOR, "input#age-id")
    choose_background = PageElement(By.CSS_SELECTOR, "input#switch_background")