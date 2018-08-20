from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


class Page:
    def __init__(self, driver, base_url):
        self.base_url = base_url
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def find_elements(self, *locator):
        return self.driver.find_elements(*locator)

    def open(self, url=''):
        url = self.base_url + url
        print('Opening: ' + url)
        self.driver.get(url)

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def wait_for_element(self, *locator):
        return self.wait.until(
            lambda self: self.find_element(*locator))

    def select_from_dropdown(self, value, *locator):
        selector = Select(self.driver.find_element(*locator))
        selector.select_by_visible_text(value)

    def wait_for_url(self, target_url):
        self.wait.until(
            EC.url_to_be(target_url))
