from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

wd = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

try:
    # Login
    wd.get("http://kitgam.kharazmico.com")
    WebDriverWait(wd, 20).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("test")
    wd.find_element(By.ID, "password").send_keys("Tt@123456")
    wd.find_element(By.XPATH, "/html/body/form/div/div[1]/div/div/div[3]/div[3]/button").click()

    # Wait for main page
    WebDriverWait(wd, 20).until(EC.url_contains("Index.do"))

    # Switch to MAIN content iframe
    WebDriverWait(wd, 20).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "content"))
    )

    # Click "New Delivers"
    new_delivers = WebDriverWait(wd, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'New Delivers')]"))
    )
    wd.execute_script("arguments[0].click();", new_delivers)

    # Switch to NESTED IFRAME
    WebDriverWait(wd, 20).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "iframe[id^='UIComponent_'][id$='_contentFrame']")
        )
    )

    # Get receiver names
    receiver_name = WebDriverWait(wd, 30).until(
        EC.visibility_of_all_elements_located(
            (
                By.XPATH,
                '//div[contains(@class, "x-grid3-cell-inner") and contains(@class, "x-grid3-col-dlrFullName")]'
            )
        )
    )

    receiver_list_name = [name.text for name in receiver_name]

    # Get all letter IDs
    letter_elements = WebDriverWait(wd, 30).until(
        EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, "div.x-grid3-cell-inner.x-grid3-col-letId")
        )
    )
    letter_ids = [elem.text for elem in letter_elements]

    # Get all sender names - IMPORTANT: We're still in the same iframe context
    sender_elements = WebDriverWait(wd, 30).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH,
             "//div[contains(@class, 'x-grid3-cell-inner') and contains(@class, 'x-grid3-col-dlvSenderFullName')]//div[contains(@class, 'longStringRender')]")
        )
    )

    sender_names = [name.text for name in sender_elements]

    # Get all time that message sent
    time_sent_elements = WebDriverWait(wd, 30).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH, '//div[contains(@class, "x-grid3-cell-inner") and contains(@class, "x-grid3-col-dlvDate")]')
        )
    )

    time_sent_list = [time.text for time in time_sent_elements]

    # Get all subjects
    subject_elements = WebDriverWait(wd, 30).until(
        EC.visibility_of_all_elements_located(
            (By.XPATH,
             '//div[contains(@class, "x-grid3-cell-inner") and contains(@class, "x-grid3-col-dlvComment")]//div[contains(@class, "longStringRender")]')
        )
    )

    subject_list = [sub.text for sub in subject_elements]  # Fixed variable name

    letters_data = []
    for i in range(len(letter_ids)):
        letter = {
            "letter_id": letter_ids[i],
            "sender": sender_names[i],
            "receiver": receiver_list_name[i],
            "time_sent": time_sent_list[i],
            "subject": subject_list[i]
        }
        letters_data.append(letter)

    for letter in letters_data:
        print(letter)


except Exception as e:
    print(f"Error: {str(e)}")
