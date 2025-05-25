import os
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class GamLetterScraper:
    def __init__(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 30)

    def login(self, username, password):
        self.driver.get("http://kitgam.kharazmico.com")
        self.wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys('test')
        self.driver.find_element(By.ID, "password").send_keys('Tt@123456')
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'ورود')]").click()
        self.wait.until(EC.url_contains("Index.do"))

    def navigate_to_letters(self):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content")))
        new_delivers = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(), 'New Delivers')]")))
        self.driver.execute_script("arguments[0].click();", new_delivers)

        self.wait.until(EC.frame_to_be_available_and_switch_to_it((
            By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']"
        )))

    def extract_letters(self):
        receivers = [el.text for el in self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "x-grid3-col-dlrFullName")]')
        ))]

        letter_ids = [el.text for el in self.wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.x-grid3-cell-inner.x-grid3-col-letId")
        ))]

        senders = [el.text for el in self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH,
             "//div[contains(@class, 'x-grid3-col-dlvSenderFullName')]//div[contains(@class, 'longStringRender')]")
        ))]

        sent_times = [el.text for el in self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "x-grid3-col-dlvDate")]')
        ))]

        subjects = [el.text for el in self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "x-grid3-col-dlvComment")]//div[contains(@class, "longStringRender")]')
        ))]

        if not all(len(lst) == len(letter_ids) for lst in [senders, receivers, sent_times, subjects]):
            raise ValueError("Mismatch in extracted data lengths.")

        return [
            {
                "letter_id": letter_ids[i],
                "sender": senders[i],
                "receiver": receivers[i],
                "time_sent": sent_times[i],
                "subject": subjects[i]
            }
            for i in range(len(letter_ids))
        ]

    def quit(self):
        self.driver.quit()

    def run(self):
        try:
            self.navigate_to_letters()
            return self.extract_letters()
        finally:
            self.quit()
