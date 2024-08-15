from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
class IMDBSearchAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def open_imdb_page(self):
        self.driver.get("https://www.imdb.com/search/name/")

    def scroll_to_element(self, xpath):
        element = self.driver.find_element(By.XPATH, xpath)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def wait_and_click_element(self, xpath, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # Scroll element into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        # Wait until the element is clickable
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        try:
            element.click()
        except Exception as e:
            # Use JavaScript click as a fallback if normal click is intercepted
            self.driver.execute_script("arguments[0].click();", element)

    def wait_and_send_keys(self, xpath, keys, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        element.send_keys(keys)

    def search_name(self, name):
        self.wait_and_click_element("//div[contains(text(),'Name')]")
        self.wait_and_send_keys("//input[@placeholder='e.g. Audrey Hepburn']", name)

    def set_birth_date_range(self, from_year, to_year):
        self.scroll_to_element("//div[contains(text(),'Birth date')]")
        self.wait_and_click_element("//div[contains(text(),'Birth date')]")
        self.wait_and_send_keys('(//input[@aria-label="Enter birth date from"])[2]', from_year)
        self.wait_and_send_keys("(//input[@aria-label='Enter birth date to'])[2]", to_year)

    def set_birthday(self, date):
        self.scroll_to_element("//div[contains(text(),'Birthday')]")
        self.wait_and_click_element("//div[contains(text(),'Birthday')]")
        self.wait_and_send_keys("//input[@placeholder='MM-DD']", date)
        self.driver.find_element(By.XPATH, "//input[@placeholder='MM-DD']").send_keys(Keys.RETURN)
        self.wait_and_click_element("//button[@data-testid='adv-search-get-results']")
        print("click is done successfully")
        self.driver.execute_script("window.scrollBy(0, -800);")

    def run(self):
        try:
            self.open_imdb_page()
            self.search_name("Ani")
            self.driver.execute_script("window.scrollBy(0, 500);")
            self.set_birth_date_range("1994", "2004")
            self.set_birthday("2004-22")


        finally:
            print("successfully executed")
            self.driver.quit()


if __name__ == "__main__":
    imdb_automation = IMDBSearchAutomation()
    imdb_automation.run()

