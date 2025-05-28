from django.http import JsonResponse
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
from letters.models import SummaryLetter
from .models import GamUser


def scrape_letters_for_user(username, password, user_id):
    options = Options()
    options.add_argument("--headless")
    wd = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    try:
        wd.get("http://kitgam.kharazmico.com")
        WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(username)
        wd.find_element(By.ID, "password").send_keys(password)
        wd.find_element(By.XPATH, "/html/body/form/div/div[1]/div/div/div[3]/div[3]/button").click()

        WebDriverWait(wd, 20).until(EC.url_contains("Index.do"))
        WebDriverWait(wd, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content")))
        new_delivers = WebDriverWait(wd, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'New Delivers')]"))
        )
        wd.execute_script("arguments[0].click();", new_delivers)

        WebDriverWait(wd, 20).until(
            EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
            )
        )

        letters_data = []

        total_pages = int(WebDriverWait(wd, 20).until(
            EC.visibility_of_element_located((By.ID, "ext-gen76"))
        ).text.split()[-1])

        for current_page in range(1, total_pages + 1):
            receiver_names = WebDriverWait(wd, 30).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "x-grid3-col-dlrFullName")]'))
            )
            receiver_list_name = [name.text for name in receiver_names]

            letter_elements = WebDriverWait(wd, 30).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.x-grid3-col-letId"))
            )
            letter_ids = [elem.text for elem in letter_elements]

            sender_elements = WebDriverWait(wd, 30).until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, "//div[contains(@class, 'x-grid3-col-dlvSenderFullName')]//div"))
            )
            sender_names = [elem.text for elem in sender_elements]

            time_sent_elements = WebDriverWait(wd, 30).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class, 'x-grid3-col-dlvDate')]"))
            )
            time_sent_list = [elem.text for elem in time_sent_elements]

            for i in range(len(letter_ids)):
                letters_data.append({
                    "letter_id": letter_ids[i],
                    "sender": sender_names[i],
                    "receiver": receiver_list_name[i],
                    "sent_time": time_sent_list[i],
                })

            if current_page == total_pages:
                break

            page_input = WebDriverWait(wd, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'x-tbar-page-number'))
            )
            page_input.clear()
            page_input.send_keys(str(current_page + 1))
            page_input.send_keys(Keys.RETURN)

            WebDriverWait(wd, 30).until(
                EC.staleness_of(letter_elements[0])
            )

            wd.switch_to.default_content()
            WebDriverWait(wd, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "content")))
            WebDriverWait(wd, 20).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
                )
            )

        # Save to database
        for item in letters_data:
            if not SummaryLetter.objects.filter(letter_id=item['letter_id'], sent_time=item['sent_time']).exists():
                SummaryLetter.objects.create(
                    letter_id=item['letter_id'],
                    user_id=user_id,
                    sender=item['sender'],
                    receiver=item['receiver'],
                    sent_time=item['sent_time'],
                )

        return {"status": "success", "letters": letters_data}

    except Exception as e:
        return {"status": "error", "message": str(e)}




def all_gam_users(request):
    all_users = GamUser.objects.all()
    list = []
    for user in all_users:
        scrape_letters_for_user(username=user.username, user_id=user.id, password=user.password)
        list.append(user.username)

    return JsonResponse({'status': 'success', 'users': list})
