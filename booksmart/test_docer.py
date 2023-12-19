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
import os
import glob
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException,   NoSuchShadowRootException
from shiftlab_ocr.doc2text.reader import Reader
from PIL import Image
# def scrap(request):
def book_scrap(author_book_docer, title_download_docer):
    # chrome_options = Options()
    chrome_options = uc.ChromeOptions()


    chrome_options.headless = False
    chrome_options.page_load_strategy = 'none'
    # options.page_load_strategy = 'eager'
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    chrome_options.add_argument("--excludeSwitches=['enable-automation']")
    chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--window-size=1280,720")
    # chrome_options.window_size="1280,720"
    chrome_options.add_argument('--incognito') 
    # chrome_options.add_argument('--verbose')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--deny-permission-prompts")
    # chrome_options.add_argument("--disable-crash-reporter")
    # # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-in-process-stack-traces")
    # chrome_options.add_extention("CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx")
    # chrome_options.add_argument("--disable-logging")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--log-level=3")

    # # Exclude the collection of enable-automation switches 
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    # chrome_options.add_experimental_option("useAutomationExtension", False) 
    chrome_options.add_experimental_option("prefs", {
    # "download.default_directory": r"C:\Users\xxx\downloads\Test",
    # "download.default_directory": "C:\Users\BONUM\Downloads\",
    # "download.default_directory": r"C:\Users\BONUM\Downloads",
    "download.prompt_for_download": False,
    # "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
    })
    # path_to_extension = r'H:\virtual2\SELENIUM\1.54.0_1'
    # chrome_options.add_argument("--embedded-extension-options")
    # path_to_extension = r"https://chromewebstore.google.com/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm"
    # chrome_options.add_argument(path_to_extension)
    # chrome_options.add_argument('load-extension=' + path_to_extension)
    chrome_options.add_extension(r'H:/virtual2/SELENIUM/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx')
    time.sleep(10)
    # driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()), )
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = uc.Chrome(desired_capabilities=capa, options=chrome_options)
    # driver = uc.Chrome(options=chrome_options)
    # driver.set_window_size(1280, 720)
    action = ActionChains(driver)
    time.sleep(1.4)
    driver.maximize_window()
    time.sleep(1.2)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    driver.execute_script("Object.defineProperty(navigator, 'uc', {get: () => undefined})") 
    # driver.get("https://docer.pl/")

    # driver.implicitly_wait(2)
    url = r"https://docer.pl/"
    time.sleep(2.1)
    log = ()
    logs = [('booksmart01', 'Djangoapp01d'), ('booksmart02', 'Djangoapp02d'), ('booksmart03', 'Djangoapp03d'),('booksmart01@hotmail.com', 'Djangoapp01d'), ('booksmart02@hotmail.com', 'Djangoapp02d'), ('booksmart03@hotmail.com', 'Djangoapp03d'), ('booksmart02', 'Djangoapp02d'), ('booksmart02@hotmail.com', 'Djangoapp02d')]
    random.shuffle(logs)
    log = random.choice(logs)
    print("log =", log)
    time.sleep(1.7)
    driver.get(url)
    time.sleep(12.4)
    try:
        # btn_cookies = WebDriverWait(driver, 5.6).until(EC.element_to_be_clickable((By.XPATH, "//button[@mode='primary']"))) # visibility_of_element_located
        # btn_cookies = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.XPATH, "//button[@mode='primary']")))
        btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
        if btn_cookies:
            print("YES //button[@mode='primary']")
            driver.execute_script("arguments[0].click();", btn_cookies)

            time.sleep(2.2)
            # driver.set_window_size(800, 600)
            time.sleep(4.2)
            try:
                # btn_login = WebDriverWait(driver, 5.6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body > nav.main-header.sticky > div > nav > ul > li:nth-child(2) > a')))
                # btn_login = driver.find_element(By.CSS_SELECTOR, '//*[@id="body"]/nav[2]/div/nav/ul/li[2]/a')
                btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')

                if btn_login:
                    print("btn_login")

                    driver.execute_script("arguments[0].click()", btn_login)

                    time.sleep(1.9)
                    username_input = driver.find_element(By.ID, "user_email")
                    print("1a. username_input")
                    if username_input:
                        print("1b. username_input")
                        action.move_to_element(username_input)
                        action.click(username_input)
                        action.perform()
                        time.sleep(0.3)
                        username_input.send_keys(log[0])
                    # else:
                    #     time.sleep(3.1)
                    #     username_input = driver.find_element(By.ID, "user_email")
                    #     print("2a. username_input")
                    #     if username_input:
                    #         print("2b. username_input")
                    #         action.move_to_element(username_input)
                    #         action.click(username_input)
                    #         action.perform()
                    #         time.sleep(0.3)
                    #         username_input.send_keys(log[0])
                    #     else:
                    #         print("NO username_input")
                    time.sleep(1.4)

                    password_input = driver.find_element(By.ID, "user_password")
                    if password_input:
                        action.move_to_element(password_input)
                        time.sleep(0.5)
                        action.click(password_input)
                        action.perform()
                        time.sleep(0.4)
                        password_input.send_keys(log[1])
                    # else:
                    #     time.sleep(3.1)
                    #     password_input = driver.find_element(By.ID, "user_password")
                    #     if password_input:
                    #         action.move_to_element(password_input)
                    #         time.sleep(0.5)
                    #         action.click(password_input)
                    #         action.perform()
                    #         time.sleep(0.4)
                    #         password_input.send_keys(log[1])
                    #     else:
                    #         print("NO password_input")

                    time.sleep(1.2)
                    remember_input = driver.find_element(By.ID, "user_remember")
                    if remember_input.is_selected():
                        
                        print("checkbox is selected")
                    else:
                        print("checkbox is unselected")            
                    submit = driver.find_element(By.ID, "login_submit")
                    action.move_to_element(submit)
                    time.sleep(0.4)
                    action.click(submit)
                    action.perform()
                    time.sleep(1.4)
            except NoSuchElementException:
                print(f"except no such element btn_login")
                time.sleep(10.2)
                btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')
                try:
                    if btn_login:
                        # action.move_to_element(btn_login).perform()
                        time.sleep(1.2)
                        action.move_to_element(btn_login)
                        action.click(btn_login)
                        action.perform()
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
                        submit = driver.find_element(By.ID, "login_submit")
                        action.move_to_element(submit)
                        time.sleep(0.4)
                        action.click(submit)
                        action.perform()
                        time.sleep(1.4)
 
                except NoSuchElementException:
                    print(f"2. except no such element btn_login")
                    try:
                        dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
                        action.move_to_element(dissmiss_button)
                        time.sleep(0.3)
                        action.click(dissmiss_button)
                        action.perform()
                        time.sleep(1.9)
                        
                    except NoSuchElementException:
                        print(f"except no such element dissmiss_button")
                           
                    time.sleep(3.4)
                    try:
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
                        submit = driver.find_element(By.ID, "login_submit")
                        action.move_to_element(submit)
                        time.sleep(0.4)
                        action.click(submit)
                        action.perform()
                        time.sleep(1.4)
                    except NoSuchElementException:
                        print(f"3. except no such element btn_login")
                        book_scrap.pdf_url_download_found = "pdf link unfinished"
    #                  print(f"1. Exception as {e}")
    except TimeoutException:
        print(f"except no such element button[@mode='primary']")
        time.sleep(1.1)
        try:
            # btn_cookies = WebDriverWait(driver, 5.6).until(EC.element_to_be_clickable((By.XPATH, "//button[@mode='primary']"))) # visibility_of_element_located
            btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
            if btn_cookies:
                print("YES //button[@mode='primary']")
                time.sleep(1.3)
                
                try:
                    btn_login = driver.find_element(By.CSS_SELECTOR, '#body > nav.main-header.sticky > div > nav > ul > li:nth-child(2) > a')
                    
                    if btn_login:
                        print("btn_login")

                        driver.execute_script("arguments[0].click()", btn_login)

                        time.sleep(1.9)
                        username_input = driver.find_element(By.ID, "user_email")
                        print("1a. username_input")
                        if username_input:
                            print("1b. username_input")
                            action.move_to_element(username_input)
                            action.click(username_input)
                            action.perform()
                            time.sleep(0.3)
                            username_input.send_keys(log[0])

                        time.sleep(1.4)

                        password_input = driver.find_element(By.ID, "user_password")
                        if password_input:
                            action.move_to_element(password_input)
                            time.sleep(0.5)
                            action.click(password_input)
                            action.perform()
                            time.sleep(0.4)
                            password_input.send_keys(log[1])


                        time.sleep(1.2)
                        remember_input = driver.find_element(By.ID, "user_remember")
                        if remember_input.is_selected():
                            
                            print("checkbox is selected")
                        else:
                            print("checkbox is unselected")            
                        submit = driver.find_element(By.ID, "login_submit")
                        action.move_to_element(submit)
                        time.sleep(0.4)
                        action.click(submit)
                        action.perform()
                        time.sleep(1.4)
                except NoSuchElementException:
                    print(f"4. except no such element btn_login")
                    book_scrap.pdf_url_download_found = "pdf link unfinished"

        except NoSuchElementException:
            print(f"except no such element btn_cookies")
            time.sleep(1.1)
            try:
                dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
                action.move_to_element(dissmiss_button)
                time.sleep(0.3)
                action.click(dissmiss_button)
                action.perform()
                time.sleep(1.9)
            # driver.get(f'https://docer.pl/show/?q={title.replace(" ", "+")}&ext=pdf')
            except NoSuchElementException:
                print(f"except no such element btn_cookies")

            time.sleep(1.1)

            try:
                # btn_login = driver.find_element(By.CSS_SELECTOR, '.btn_show_login')
                btn_login = WebDriverWait(driver, 5.6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body > nav.main-header.sticky > div > nav > ul > li:nth-child(2) > a')))
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
                submit = driver.find_element(By.ID, "login_submit")
                action.move_to_element(submit)
                time.sleep(0.4)
                action.click(submit)
                action.perform()
                time.sleep(1.4)

            # except Exception as e:
            except TimeoutException:
                print(f"except no such element btn_login")
                try:
                    btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')
                    if btn_login:
                        action.move_to_element(btn_login).perform()
                        driver.execute_script("arguments[0].click()", btn_login)
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
                        submit = driver.find_element(By.ID, "login_submit")
                        action.move_to_element(submit)
                        time.sleep(0.4)
                        action.click(submit)
                        action.perform()
                        time.sleep(1.4)
                except NoSuchElementException:
                    print(f"2 except no such element btn_login")
                    book_scrap.pdf_url_download_found = "pdf link unfinished"
                    time.sleep(10)
                    driver.close()

    time.sleep(4.6)
    # driver.set_window_size(1024, 720)
    try:
        book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
        print("book_to_search =", book_to_search)
        # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
        url_pdfs = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'
        time.sleep(5.4)
        # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
        print("urls_pdf =", url_pdfs)
        print("author_book_docer =", author_book_docer)
        driver.get(url_pdfs)
        time.sleep(9.8)

        # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')

        # text_contains = f'//*[contains(text(), "{author_book_docer}")]'
        # text_contains = '//*[@id="item-section"]/li[*]/div/div/div[2]/h3/a[contains(text(), "{author_book_docer}")]'
        # text_contains = '//*[@id="item-section"]/*/div/div/div[2]/h3/a[contains(text(), "{author_book_docer}")]'
        # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
        
        # link_first = WebDriverWait(driver, 9.2).until(EC.visibility_of_element_located((By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')))
        # driver.set_window_size(800, 600)
        
        try:
            captcha_input_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
            if captcha_input_1:
                print("1. captcha_input_1")
                time.sleep(12.2)
                captcha_img_1 = captcha_input_1.find_element(By.XPATH, "preceding-sibling::*[1]")
                print("captcha_img_1 src =", captcha_img_1.get_attribute("src"))
                # captcha_screenshot_1 = captcha_img_1.screenshot("screenshot_captcha.png")
                captcha_screenshot_1 = captcha_img_1.screenshot_as_png('captcha_img.png')
                
                time.sleep(1.2)
                captcha_image_1 = Image.open(captcha_screenshot_1)

                # captcha_imageStram = io.BytesIO(captcha_screenshot_1)
                # captcha_image_1 = Image.open(captcha_imageStram)
                
                time.sleep(1.4)
                reader = Reader()

                result_recaptcha = reader.doc2text(captcha_image_1)

                print("result_recaptcha[0] =", result_recaptcha[0])
                # captcha_input_1.send_keys()
                # captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
                # driver.execute_script("arguments[0].click()", captcha_submit_1)
                time.sleep(90)
            else:
                print("NO captcha_1")
        except NoSuchElementException:
            print(f"except NoSuchElementException captcha_1")

        try:    
            text_contains = f'//a[contains(text(), "{author_book_docer}")]'
            print("2. text_contains =", text_contains)
            time.sleep(0.6)
            link_first = driver.find_element(By.XPATH, text_contains)
            if link_first:
                print("1. link_first")
                file_name = link_first.text
                print("1. file_name =", file_name)
                driver.execute_script("arguments[0].click();", link_first)
                print("1. CLICK link first")
                # a.move_to_element(link_first).click().perform()
                # link_first.click()
                # action.move_to_element(link_first)
                # time.sleep(0.3)
                # action.click(link_first)
                # action.perform()
                # time.sleep(1.4)
                time.sleep(12.2)
            else:
                print("1. NO link_first")
        
        except NoSuchElementException:
            print("1. NoSuchElementException link_first")
            try:
                text_contains = f'//*[contains(text(), "{author_book_docer}")]'
                print("2. text_contains =", text_contains)
                time.sleep(0.8)
                link_first = driver.find_element(By.XPATH, text_contains)
                if link_first:
                    print("2. link_first")
                    file_name = link_first.text
                    print("2. file_name =", file_name)
                    driver.execute_script("arguments[0].click();", link_first)
                    print("2. CLICK link first")
                    # a.move_to_element(link_first).click().perform()
                    # link_first.click()
                    # action.move_to_element(link_first)
                    # time.sleep(0.3)
                    # action.click(link_first)
                    # action.perform()
                    # time.sleep(1.4)
                    time.sleep(12.2)
                else:
                    print("1. NO link_first")
            except NoSuchElementException:
                print("2 NoSuchElementException link_first")

                try:
                    captcha_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
                    if captcha_1:
                        time.sleep(20)
                        # chrome_options.set_attribute('--headless', False)
                        time.sleep(90)
                    else:
                        print("NO captcha_1")
                except NoSuchElementException:
                    print(f"except NoSuchElementException captcha_1")
                    # link_first = WebDriverWait(driver, 9.2).until(EC.visibility_of_element_located((By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')))
                    # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
                try:
                    text_contains = f'//*[contains(text(), "{author_book_docer}")]'
                    print("2. text_contains =", text_contains)
                    time.sleep(0.6)
                    # text_contains = '//*[@id="item-section"]/li[*]/div/div/div[2]/h3/a[contains(text(), "{author_book_docer}")]'
                    # text_contains = '//*[@id="item-section"]/*/div/div/div[2]/h3/a[contains(text(), "{author_book_docer}")]'
                    # text_contains = f'//*[contains(text(), "{author_book_docer}")]'
                    # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
                    link_first = driver.find_element(By.XPATH, text_contains)
                    if link_first:
                        print("2. link_first")
                        file_name = link_first.text
                        print("2. file_name =", file_name)
                        # link_first.click()   
                        driver.execute_script("arguments[0].click();", link_first) 
                        time.sleep(10.6)        
                    else:
                        print("2. NO link_first")

                # except TimeoutException:
                #     print("3a. TimeoutException")
                #     time.sleep(10)
                except NoSuchElementException:
                    print("2b. NoSuchElementException")
                    time.sleep(10.9)  
                    try:
                        link_first = WebDriverWait(driver, 9.2).until(EC.visibility_of_element_located((By.XPATH, f'//*a[contains(text(), "{author_book_docer}")]')))
                        if link_first:
                            print("3. link_first")
                            file_name = link_first.text
                            print("3. file_name =", file_name)
                            driver.execute_script("arguments[0].click();", link_first)
                            # a.move_to_element(link_first).click().perform()
                            # link_first.click()
                            # action.move_to_element(link_first)
                            # time.sleep(0.3)
                            # action.click(link_first)
                            # action.perform()
                            # time.sleep(1.4)
                        else:
                            print("NO link_first")
                            time.sleep(10)
                            driver.close()
                    except TimeoutException:
                        print(f"3a. TimeoutException")
                        book_scrap.pdf_url_download_found = "no pdf link docer"
                        time.sleep(6.7)
                        driver.close()
            


    except Exception as e:
        print(f"Exception as {e}")
        time.sleep(11.6)
        print("NO LINK FIRST")


    time.sleep(9.2) 
    # driver.set_window_size(800, 600)

    try:
        captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
        if captcha_input_2:
            print("1. captcha_input_2")
            time.sleep(12.2)
            captcha_img_2 = captcha_input_2.find_element(By.XPATH, "preceding-sibling::*[1]")
            print("captcha_img_2 src =", captcha_img_2.get_attribute("src"))
            # captcha_screenshot_1 = captcha_img_1.screenshot("screenshot_captcha.png")
            captcha_screenshot_2 = captcha_img_2.screenshot_as_png('captcha_img_2.png')
            
            time.sleep(1.2)
            captcha_image_2 = Image.open(captcha_screenshot_2)

            # captcha_imageStram = io.BytesIO(captcha_screenshot_1)
            # captcha_image_1 = Image.open(captcha_imageStram)
            
            time.sleep(1.4)
            reader_2 = Reader()

            result_recaptcha_2 = reader_2.doc2text(captcha_image_2)

            print("result_recaptcha_2[0] =", result_recaptcha_2[0])
            # captcha_input_1.send_keys()
            # captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
            # driver.execute_script("arguments[0].click()", captcha_submit_1)
            time.sleep(90)
        else:
            print("NO captcha_input_2")
    except NoSuchElementException:
        print(f"except NoSuchElementException captcha_2")
    time.sleep(2.1)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        btn_download = driver.find_element(By.ID, "dwn_btn")
        # btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
        # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
        if btn_download:
            driver.execute_script("return arguments[0].scrollIntoView(true);", btn_download)
            print("1. btn_download")
            book_scrap.get_current_url = driver.current_url
            print("1. get_url =", book_scrap.get_current_url)

            action.move_to_element(btn_download)
            action.perform()
            driver.execute_script("arguments[0].click()", btn_download)
            # action.release()
            
            time.sleep(1.3)

            try:
                elem_right = driver.find_element(By.CSS_SELECTOR, "#watch7-sidebar-contents > div > div")
                if elem_right:
                    print("3. elem_right")
                    action.move_to_element(elem_right)
                    action.perform()
            except NoSuchElementException:
                print("3. elem_right NoSuchElementException")

            time.sleep(12.6)
            # driver.set_window_size(1024, 720)
            time.sleep(28.2)
            
            # try:
            #     div_captcha = driver.find_element(By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-border")
            #     if div_captcha:
            #         action.move_to_element(div_captcha)
            #         action.click(div_captcha)
            #         action.perform()
            #         time.sleep(1.6)
            #         elem_right = driver.find_element(By.CSS_SELECTOR, "#watch7-sidebar-contents > div > div")
            #         action.move_to_element(elem_right)
            #         action.perform()
            #     else:
            #         print("NO div_captcha")
            # except NoSuchElementException:
            #     print("NoSuchElementException div_captcha")
            time.sleep(14.2)
            try:
                driver.execute_script("window.open()")
                driver.switch_to.window(driver.window_handles[1])
                driver.get("chrome://downloads/")
                time.sleep(9.4)
                try:
                    downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
                    if downloaded_book:
                        book_scrap.pdf_url_download_found = downloaded_book.get_attribute("href")
                        print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
                        file_name_found = downloaded_book.text
                        print("file_name_found =", file_name_found)
                        try:
                            show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
                            driver.execute_script("arguments[0].click()", show_book_my)
                        except NoSuchElementException:
                            print(f"NoSuchElementException show_book_my") 

                        # if file_name_found[:len(file_name)] == file_name:
                        if file_name in file_name_found:
                            pdf_url_download = book_scrap.pdf_url_download_found
                            print(f'pdf_url_download = {pdf_url_download}')
                            print("SUCCESS !!! " * 5)
                            # driver.execute_script("arguments[0].click()", downloaded_book)
                            time.sleep(10)
                            try:
                                show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
                                if show_book:
                                    print("show_book.text =", show_book.text)
                                    driver.execute_script("arguments[0].click()", show_book)
                                    time.sleep(20)
                                    driver.close()
                                else:
                                    print("NO show_book")
                            except NoSuchElementException:
                                print(f"NoSuchElementException show_book_my") 
                                time.sleep(9)
                                driver.close()
                    else:
                        time.sleep(3.4)
                        print("NO downloaded_book")

                except NoSuchShadowRootException:
                    print("1. NoSuchShadowRootException downloaded_book") 
                    try:
                        downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
                        if downloaded_book:
                            book_scrap.pdf_url_download_found = downloaded_book.get_attribute("href")
                            print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
                            file_name_found = downloaded_book.text
                            print("file_name_found =", file_name_found)

                            try:
                                show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
                                driver.execute_script("arguments[0].click()", show_book_my)
                            except NoSuchElementException:
                                print(f"NoSuchElementException show_book_my") 

                            if file_name_found[:len(file_name)+1] == file_name:
                                pdf_url_download = book_scrap.pdf_url_download_found
                                print(f'pdf_url_download = {pdf_url_download}')
                                print("SUCCESS !!! " * 5)
                                # driver.execute_script("arguments[0].click()", downloaded_book)
                                time.sleep(10)
                                try:
                                    show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
                                    if show_book:
                                        print("show_book.text =", show_book.text)
                                        driver.execute_script("arguments[0].click()", show_book)
                                        time.sleep(20)
                                        driver.close()
                                    else:
                                        print("NO show_book")
                                except NoSuchElementException:
                                    print(f"NoSuchElementException show_book_my") 
                                    time.sleep(9)
                                    driver.close()

                    except NoSuchShadowRootException:
                        print("2. NoSuchShadowRootException downloaded_book") 
                        book_scrap.pdf_url_download_found = "pdf link exist"

            except Exception as e:
                print("Exception window.open()")
                book_scrap.pdf_url_download_found = "pdf link exist"
                 
    except NoSuchElementException:
        print("NoSuchElementException btn_dwn FIRST") 
        try:
            element_link_end = driver.find_element(By.ID, "iframe2")
            if element_link_end:
                element_link_end_outer = element_link_end.get_attribute("outerHTML")
                print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
                link_end = element_link_end.get_attribute('data-pdf-url')
                if link_end != None:
                    print('1. link_end =', link_end)
                    time.sleep(2.6)
                    driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
                else:
                    print('2. link_end = None')
                    time.sleep(9.3)
                    element_link_end = driver.find_element(By.ID, "iframe2")
                    if element_link_end:
                        element_link_end_outer = element_link_end.get_attribute("outerHTML")
                        print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
                        link_end = element_link_end.get_attribute('data-pdf-url')
                        if link_end_3!= None:
                            print('2. link_end =', link_end)
                            driver.execute_script("window.scrollTo(300, document.body.scrollHeight);")
                        else:     
                            print('2. link_end = None')         
        except NoSuchElementException:
            print("NoSuchElementException link_end") 
        try:
            btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
            # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
            # btn_download = driver.find_element(By.ID, "dwn_btn")
            if btn_download:
                driver.execute_script("return arguments[0].scrollIntoView(true);", btn_download)
                print("1. btn_download")
                driver.execute_script("window.scrollTo(260, document.body.scrollHeight);")
                book_scrap.get_current_url = driver.current_url
                print("2. get_url =", get_url)
                action.move_to_element(btn_download)
                action.perform()
                driver.execute_script("arguments[0].click()", btn_download)
                # action.release()
                
                time.sleep(1.3)
                try:
                    elem_right = driver.find_element(By.CSS_SELECTOR, "#watch7-sidebar-contents > div > div")
                    if elem_right:
                        print("2. elem_right")
                        action.move_to_element(elem_right)
                        action.perform()
                except NoSuchElementException:
                    print("2. elem_right NoSuchElementException")
                    time.sleep(32)

                # try:
                #     div_captcha = driver.find_element(By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-border")
                #     if div_captcha:
                #         action.move_to_element(div_captcha)
                #         action.click(div_captcha)
                #         action.perform()
                #         time.sleep(1.6)
                #         elem_right = driver.find_element(By.CSS_SELECTOR, "#watch7-sidebar-contents > div > div")
                #         action.move_to_element(elem_right)
                #         action.perform()
                #     else:
                #         print("NO div_captcha")
                # except NoSuchElementException:
                #     print("NoSuchElementException div_captcha")
                time.sleep(14.2)
                try:
                    driver.execute_script("window.open()")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get("chrome://downloads/")
                    time.sleep(10)
                    try:
                        downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
                        if downloaded_book:
                            book_scrap.pdf_url_download_found = downloaded_book.get_attribute("href")
                            print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
                            file_name_found = downloaded_book.text
                            print("file_name_found =", file_name_found)
                            try:
                                show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
                                driver.execute_script("arguments[0].click()", show_book_my)
                            except Exception as e:
                                print(f"show_book_my except btn_download: Exception as {e}") 

                            if file_name_found[:len(file_name)+1] == file_name:
                                pdf_url_download = book_scrap.pdf_url_download_found
                                print(f'pdf_url_download = {pdf_url_download}')
                                print("SUCCESS !!! " * 5)
                                # driver.execute_script("arguments[0].click()", downloaded_book)
                                time.sleep(10)
                                show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
                                driver.execute_script("arguments[0].click()", show_book_my)
                                show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
                                if show_book:
                                    print("show_book.text =", show_book.text)
                                    driver.execute_script("arguments[0].click()", show_book)
                                    time.sleep(20)
                                    driver.close()
                                else:
                                    print("NO show_book")
                    except NoSuchElementException:
                        print(f"NoSuchElementException downloaded_book") 
                        book_scrap.pdf_url_download_found = "pdf link exist"
                except Exception as e:
                    print("Exception window.open()")   
                    book_scrap.pdf_url_download_found = "pdf link exist"
        except TimeoutException:
            print("TimeoutException btn_dwn FIRST")
            book_scrap.pdf_url_download_found = "pdf link exist"
            time.sleep(20)
            driver.close()
    
    time.sleep(20)
    try:
        home = os.path.expanduser("~")
        downloadspath=os.path.join(home, "Downloads")
        list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
        name_last_file = latest_file.split("\\")[-1][:-4]
        if name_last_file[:len(file_name)+1] == file_name:
            print("SUCCESS !!! " * 10)
    except Exception as e:
         print(f"except last check chrome-downloads: Exception as {e}") 

    time.sleep(2.1)
    driver.quit()





# # author_book_docer_full = "Ernest Hemingway"
# # author_book_docer = author_book_docer_full.split()[-1]
# author_book_docer = "Sapkowski"
# print("author_book_docer =", author_book_docer)
# # title_download_docer = download_book.title_download_value
# title_download_docer = "Chrzest ognia"
# print("title_download_docer =", title_download_docer)
# # book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
# # print("book_to_search =", book_to_search)
# # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
# # url_wait = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'

# book_scrap(author_book_docer, title_download_docer)

# author_book_docer = "Ziemiański"
# print("author_book_docer =", author_book_docer)
# # title_download_docer = download_book.title_download_value
# title_download_docer = "Wojny urojone"
# print("title_download_docer =", title_download_docer)
# # book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
# # print("book_to_search =", book_to_search)
# # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
# # url_wait = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'
# book_scrap(author_book_docer, title_download_docer)


