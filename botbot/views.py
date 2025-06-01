# region past

# from django.http import JsonResponse
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.by import By
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.firefox import GeckoDriverManager
# from letters.models import SummaryLetter
# from .models import GamUser

# def scrape_letters_for_user(username, password, user_id):
#     options = Options()
#     options.add_argument("--headless")
#     wd = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
#
#     try:
#         wd.get("http://kitgam.kharazmico.com")
#         WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
#         wd.find_element(By.ID, "password").send_keys(password)
#         wd.find_element(By.XPATH, "/html/body/form/div/div[1]/div/div/div[3]/div[3]/button").click()
#
#         WebDriverWait(wd, 20).until(EC.url_contains("Index.do"))
#         WebDriverWait(wd, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content")))
#         new_delivers = WebDriverWait(wd, 20).until(
#             EC.element_to_be_clickable((By.XPATH, "//span[text()='ارجاعات جدید']"))
#         )
#
#         wd.execute_script("arguments[0].click();", new_delivers)
#
#         WebDriverWait(wd, 20).until(
#             EC.frame_to_be_available_and_switch_to_it(
#                 (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
#             )
#         )
#
#         letters_data = []
#
#         total_pages = int(WebDriverWait(wd, 20).until(
#             EC.visibility_of_element_located((By.ID, "ext-gen75"))
#         ).text.split()[-1])
#
#         for current_page in range(1, total_pages + 1):
#             receiver_names = WebDriverWait(wd, 30).until(
#                 EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "x-grid3-col-dlrFullName")]'))
#             )
#             receiver_list_name = [name.text for name in receiver_names]
#
#             letter_elements = WebDriverWait(wd, 30).until(
#                 EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.x-grid3-col-letId"))
#             )
#             letter_ids = [elem.text for elem in letter_elements]
#
#             sender_elements = WebDriverWait(wd, 30).until(
#                 EC.visibility_of_all_elements_located(
#                     (By.XPATH, "//div[contains(@class, 'x-grid3-col-dlvSenderFullName')]//div"))
#             )
#             sender_names = [elem.text for elem in sender_elements]
#
#             time_sent_elements = WebDriverWait(wd, 30).until(
#                 EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x-grid3-col-dlvDate')]"))
#             )
#             time_sent_list = [elem.text for elem in time_sent_elements]
#
#             for i in range(len(letter_ids)):
#                 letters_data.append({
#                     "letter_id": letter_ids[i],
#                     "sender": sender_names[i],
#                     "receiver": receiver_list_name[i],
#                     "sent_time": time_sent_list[i],
#                 })
#
#             if current_page == total_pages:
#                 break
#
#             page_input = WebDriverWait(wd, 20).until(
#                 EC.presence_of_element_located((By.CLASS_NAME, 'x-tbar-page-number'))
#             )
#             page_input.clear()
#             page_input.send_keys(str(current_page + 1))
#             page_input.send_keys(Keys.RETURN)
#
#             WebDriverWait(wd, 30).until(
#                 EC.staleness_of(letter_elements[0])
#             )
#
#             wd.switch_to.default_content()
#             WebDriverWait(wd, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content")))
#             WebDriverWait(wd, 20).until(
#                 EC.frame_to_be_available_and_switch_to_it(
#                     (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
#                 )
#             )
#
#         # Save to database
#         for item in letters_data:
#             if not SummaryLetter.objects.filter(letter_id=item['letter_id'], sent_time=item['sent_time']).exists():
#                 SummaryLetter.objects.create(
#                     letter_id=item['letter_id'],
#                     user_id=user_id,
#                     sender=item['sender'],
#                     receiver=item['receiver'],
#                     sent_time=item['sent_time'],
#                 )
#
#         return {"status": "success", "letters": letters_data}
#
#     except Exception as e:
#         return {"status": "error", "message": str(e)}
#
#
# def scrape_all_users(request):
#     all_users = GamUser.objects.all()
#     list = []
#     for user in all_users:
#         scrape_letters_for_user(username=user.username, user_id=user.id, password=user.password)
#         list.append(user.username)
#
#     return JsonResponse({'status': 'success', 'users': list})

# endregion

# region new

from django.core.management.base import BaseCommand
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from botbot.models import GamUser
from letters.models import SummaryLetter
import logging
from concurrent.futures import ThreadPoolExecutor
import requests
from datetime import datetime
from selenium.webdriver.common.keys import Keys

logger = logging.getLogger(__name__)


class GamScraper:
    def __init__(self):
        self.driver = self._init_driver()
        self.wait_timeout = 20
        self.notification_timeout = 10

    def _init_driver(self):
        """Initialize and configure Firefox driver"""
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")

        try:
            service = Service(GeckoDriverManager().install())
            driver = Firefox(service=service, options=options)
            driver.implicitly_wait(5)
            return driver
        except Exception as e:
            logger.error(f"Driver initialization failed: {str(e)}")
            raise

    def _login(self, username, password):
        """Handle login process"""
        try:
            self.driver.get("http://kitgam.kharazmico.com")

            WebDriverWait(self.driver, self.wait_timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            username_field = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(username)

            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)

            login_button = self.driver.find_element(
                By.XPATH, "/html/body/form/div/div[1]/div/div/div[3]/div[3]/button"
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", login_button)
            login_button.click()

            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.url_contains("Index.do")
            )
            return True
        except Exception as e:
            logger.error(f"Login failed for {username}: {str(e)}")
            return False

    def _navigate_to_letters(self):
        """Navigate to the letters section"""
        try:
            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "content"))
            )

            new_delivers = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='ارجاعات جدید']"))
            )
            self.driver.execute_script("arguments[0].click();", new_delivers)

            WebDriverWait(self.driver, self.wait_timeout).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
                )
            )
            return True
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            return False

    def _scrape_page_data(self):
        """Scrape data from current page"""
        locators = {
            'receiver': (By.XPATH, '//div[contains(@class, "x-grid3-col-dlrFullName")]'),
            'letter_id': (By.CSS_SELECTOR, 'div.x-grid3-col-letId'),
            'sender': (By.XPATH, '//div[contains(@class, "x-grid3-col-dlvSenderFullName")]//div'),
            'sent_time': (By.XPATH, '//div[contains(@class, "x-grid3-col-dlvDate")]')
        }

        data = {}
        for field, locator in locators.items():
            try:
                elements = WebDriverWait(self.driver, self.wait_timeout).until(
                    EC.presence_of_all_elements_located(locator)
                )
                data[field] = [e.text for e in elements]
            except Exception as e:
                logger.error(f"Failed to scrape {field}: {str(e)}")
                data[field] = []

        return [
            {
                'letter_id': data['letter_id'][i],
                'sender': data['sender'][i],
                'receiver': data['receiver'][i],
                'sent_time': data['sent_time'][i]
            }
            for i in range(len(data['letter_id']))
        ]

    def _get_total_pages(self):
        """Get total number of pages"""
        try:
            total_pages_text = WebDriverWait(self.driver, self.wait_timeout).until(
                EC.presence_of_element_located((By.ID, "ext-gen75"))
            ).text
            return int(total_pages_text.split()[-1])
        except Exception as e:
            logger.error(f"Failed to get total pages: {str(e)}")
            return 1

    def scrape_user_letters(self, username, password, user_id):
        """Main scraping method"""
        try:
            if not self._login(username, password):
                return {"status": "error", "message": "Login failed"}

            if not self._navigate_to_letters():
                return {"status": "error", "message": "Navigation failed"}

            total_pages = self._get_total_pages()
            all_letters = []

            for current_page in range(1, total_pages + 1):
                page_letters = self._scrape_page_data()
                all_letters.extend(page_letters)

            new_letters = []
            user = GamUser.objects.get(id=user_id)

            for letter in all_letters:
                if not SummaryLetter.objects.filter(
                        letter_id=letter['letter_id'],
                        sent_time=letter['sent_time']
                ).exists():
                    SummaryLetter.objects.create(
                        letter_id=letter['letter_id'],
                        user_id=user_id,
                        sender=letter['sender'],
                        receiver=letter['receiver'],
                        sent_time=letter['sent_time'],
                    )
                    new_letters.append(letter)

            return {
                "status": "success",
                "total_letters": len(all_letters),
                "new_letters": len(new_letters),
                "user_id": user_id
            }

        except Exception as e:
            logger.error(f"Scraping failed for {username}: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            self.driver.quit()


class Command(BaseCommand):
    help = 'Scrape GAM letters for all active users'

    def handle(self, *args, **options):
        start_time = datetime.now()
        users = GamUser.objects.filter(is_active=True)
        results = []

        scraper = GamScraper()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for user in users:
                futures.append(executor.submit(
                    scraper.scrape_user_letters,
                    user.username,
                    user.password,
                    user.id
                ))

            for future in futures:
                try:
                    results.append(future.result())
                except Exception as e:
                    logger.error(f"Processing failed: {str(e)}")
                    results.append({"status": "error", "message": str(e)})

        scraper.driver.quit()
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"Scraping completed in {duration:.2f} seconds")

        self.stdout.write(self.style.SUCCESS(
            f"Processed {len(users)} users with {sum(r.get('new_letters', 0) for r in results)} new letters"
        ))


# endregion
