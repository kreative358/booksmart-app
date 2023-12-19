import requests, random, time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
import os.path
import undetected_chromedriver as uc


# def scrap(request):
def book_scrap(author_book_docer, title_download_docer):
    # chrome_options = Options()
    chrome_options = uc.ChromeOptions()
    chrome_options.headless = False
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("excludeSwitches=['enable-automation']")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument('--incognito') 
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument('--incognito')

    # chrome_options.add_argument("--disable-crash-reporter")
    # # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    # chrome_options.add_argument("--disable-logging")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--log-level=3")

    # # Exclude the collection of enable-automation switches 
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # chrome_options.add_experimental_option("useAutomationExtension", False) 
    # chrome_options.add_experimental_option("prefs", {
    # # "download.default_directory": r"C:\Users\xxx\downloads\Test",
    # "download.prompt_for_download": False,
    # "download.directory_upgrade": True,
    # # "safebrowsing.enabled": True,
    # "safebrowsing_for_trusted_sources_enabled": False,
    # "safebrowsing.enabled": False
    # })
    # path_to_extension = r'H:\virtual2\SELENIUM\1.54.0_1'
    # chrome_options.add_argument('load-extension=' + path_to_extension)

    # driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()), )
    driver = uc.Chrome(options=chrome_options)
    # driver.set_window_size(1280, 720)
    driver.maximize_window()

    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    driver.execute_script("Object.defineProperty(navigator, 'uc', {get: () => undefined})") 
    # driver.get("https://docer.pl/")

    # driver.implicitly_wait(2)
    url = r"https://docer.pl/"
    time.sleep(5)
    log = ()
    logs = [('booksmart01', 'Djangoapp01d'), ('booksmart02', 'Djangoapp02d'), ('booksmart03', 'Djangoapp03d'),('booksmart01@hotmail.com', 'Djangoapp01d'), ('booksmart02@hotmail.com', 'Djangoapp02d'), ('booksmart03@hotmail.com', 'Djangoapp03d'), ('booksmart02', 'Djangoapp02d'), ('booksmart02@hotmail.com', 'Djangoapp02d')]
    random.shuffle(logs)
    log = random.choice(logs)
    print("log =", log)
    time.sleep(1.7)
    driver.get(url)
    try:
        btn_cookies = WebDriverWait(driver, 5.4).until(EC.element_to_be_clickable((By.XPATH, "//button[@mode='primary']")))
        if btn_cookies:
            print("YES //button[@mode='primary']")
            # btn_cookies.click()
            driver.execute_script("arguments[0].click();", btn_cookies)
            btn_login = driver.find_element(By.XPATH, '//*[@id="body"]/nav[2]/div/nav/ul/li[2]/a')
            btn_login.click()
            time.sleep(1.7)
            username_input = driver.find_element(By.ID, "user_email").send_keys(log[0])
            time.sleep(1.4)
            password_input = driver.find_element(By.ID, "user_password").send_keys(log[1])
            time.sleep(1.2)
            remember_input = driver.find_element(By.ID, "user_remember")
            if remember_input.is_selected():
                
                print("checkbox is selected")
            else:
                print("checkbox is unselected")
        else:
            print("NO //button[@mode='primary']")
            btn_login = driver.find_element(By.XPATH, '//*[@id="body"]/nav[2]/div/nav/ul/li[2]/a')
            btn_login.click()
            time.sleep(1.7)
            username_input = driver.find_element(By.ID, "user_email").send_keys(log[0])
            time.sleep(1.4)
            password_input = driver.find_element(By.ID, "user_password").send_keys(log[1])
            time.sleep(1.2)
            remember_input = driver.find_element(By.ID, "user_remember")
            if remember_input.is_selected():
                
                print("checkbox is selected")
            else:
                print("checkbox is unselected")
            return driver
    except Exception as e:
        print(f"1. Exception as {e}")
        # driver.get(f'https://docer.pl/show/?q={title.replace(" ", "+")}&ext=pdf')
        time.sleep(2.3)
        driver.close()

    time.sleep(2.6)
    try:
        
        book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
        print("book_to_search =", book_to_search)
        # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
        url_wait = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'
        time.sleep(5.4)
        # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
        print("url_wait =", url_wait)
        print("author_book_docer =", author_book_docer)
        driver.get(url_wait)
        time.sleep(10)

        link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
        if link_first:
            print("link_first")
            file_name = link_first.text
            print("file_name =", file_name)
            
            link_first.click()
            
        else:
            print("NO link_first")
            time.sleep(10)
            driver.close()

    except Exception as e:
        print(f"2a. Exception as {e}")
        time.sleep(5.7)
        try:
            
            book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
            print("book_to_search =", book_to_search)
            # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
            url_wait = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'
            time.sleep(5.4)
            # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
            print("url_wait =", url_wait)
            print("author_book_docer =", author_book_docer)
            driver.get(url_wait)
            time.sleep(10)

            link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
            if link_first:
                print("link_first")
                file_name = link_first.text
                print("file_name =", file_name)
                
                link_first.click()
                
            else:
                print("NO link_first")
                time.sleep(10)
                driver.close()

        except Exception as e:
            print(f"2a. Exception as {e}")
            time.sleep(10)
            driver.close()

    time.sleep(7.2)

    try:
        btn_download = driver.find_element(By.ID, "dwn_btn")
        # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
        if btn_download:
            print("1. btn_download")
            driver.execute_script("arguments[0].click()", btn_download)
            time.sleep(20)
            driver.execute_script("window.open()")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("chrome://downloads/")
            time.sleep(20)
            downloaded_book = driver.find_element(By.ID, "file-link")
            print("downloaded_book.text =", downloaded_book.text)
            if downloaded_book.text == file_name:
                print(f'DOWNLOAD book title: {file_name}')
                time.sleep(10)
                driver.close()
        else:
            time.sleep(12)
            btn_download = driver.find_element(By.ID, "dwn_btn")
            # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
            if btn_download:
                print("1. btn_download")
                driver.execute_script("arguments[0].click()", btn_download)
                time.sleep(10)
                driver.close()
    except Exception as e:
        print(f"else except btn_download: Exception as {e}") 


# author_book_docer_full = "Ernest Hemingway"
# author_book_docer = author_book_docer_full.split()[-1]
# print("author_book_docer =", author_book_docer)
# # title_download_docer = download_book.title_download_value
# title_download_docer = "Wiosenne potoki"
# print("title_download_docer =", title_download_docer)
# book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
# print("book_to_search =", book_to_search)
# # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
# url_wait = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'

# book_scrap(author_book_docer, title_download_docer)


