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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchShadowRootException, ScreenshotException, JavascriptException, MoveTargetOutOfBoundsException, NoSuchDriverException, InvalidSessionIdException, SessionNotCreatedException, NoSuchAttributeException
# from shiftlab_ocr.doc2text.reader import Reader
from PIL import Image
from django.conf import settings
from django.conf.urls.static import static
# def scrap(request):
import io
import urllib.request
import easyocr
from booksmart.models import Book
from booksmart.api.serializers import BookPdfUrlSerializer
import signal
import subprocess
from requests.exceptions import RequestException, ConnectionError
from urllib3.exceptions import NewConnectionError, ConnectTimeoutError, MaxRetryError
from selenium.webdriver.remote.command import Command


def url_exists(driver_current_url, context_book_scrap_url_exist, book_pdf_bot):
    """Check if resource exist?"""
    if not driver_current_url:
        print("driver_current_url is required")
    try:
        resp = requests.head(driver_current_url)
        if resp.status_code == 200:
            print("TRUE driver_current_url")
            context_book_scrap_url_exist["link_first"] = "link first confirmed"
            return context_book_scrap_url_exist
        else:
            print("FALSE driver_current_url")            
            context_book_scrap_url_exist["link_first"] = ""    
            context_book_scrap_url_exist["file_name"] = "no pdf filename docer" 
            context_book_scrap_url_exist["link_pdf"] = ""
            try:                  
                serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
                if serializer.is_valid():
                    serializer.save() 
            except Exception as e:
                print(f"1. url_exists serializer.save() Exception as {e}")    
                               
            return context_book_scrap_url_exist
        
    except Exception as e:
        print(f"url_exists Exception as {e}")
        context_book_scrap_url_exist["link_first"] = ""    
        context_book_scrap_url_exist["file_name"] = "no pdf filename docer" 
        context_book_scrap_url_exist["link_pdf"] = ""  
        try:                
            serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': "", 'url_pdf_search': "", "url_pdf": ""}, partial=True)
            if serializer.is_valid():
                serializer.save() 
        except Exception as e:
            print(f"2. url_exists serializer.save() Exception as {e}")   
                      
        return context_book_scrap_url_exist
        

def get_pid(driver):
    chromepid = int(driver.service.process.pid)
    print("chromepid =", chromepid)
    return (chromepid)

def kill_chrome(pid):
    try:
        print("pid =", pid)
        os.kill(pid, signal.SIGTERM)
        subprocess.check_output("Taskkill /PID %d /F" % pid)
        return 1
    except Exception as e:
        print(f"Exception as {e}")
        return 0
    
# def book_scrap(book_id_book_scrap, driver, action, reader_easyocr, *args, **kwargs):
#     context_book_scrap = {}
#     context_book_scrap_url_exist = {}
#     print("def book_scrap")
#     result_bot = "result bot"
#     book_pdf_bot = Book.objects.filter(pk=book_id_book_scrap).first()
#     book_pdf_bot_values = Book.objects.filter(pk=book_id_book_scrap).values()[0]
#     print('book_pdf_bot_values["url_pdf"] =', book_pdf_bot_values["url_pdf"])
#     book_scrap.pdf_url_download_found = book_pdf_bot_values["url_pdf"]
#     book_scrap.get_current_url = book_pdf_bot_values["url_pdf_search"]
#     book_scrap.link_first_filename = book_pdf_bot_values["pdf_search_filename"]
#     author_book_docer = book_pdf_bot_values["author"].split()[-1]
#     title_book_docer = book_pdf_bot_values["title"]
#     title_download_docer = book_pdf_bot_values["title"]
    
#     context_book_scrap["login_pass"] = ""
#     context_book_scrap["driver_current_url"] = ""
#     context_book_scrap["link_end"] = "no link_end"
#     context_book_scrap["link_first"] = ""
#     context_book_scrap["show_title_path"] = ""
#     context_book_scrap["pdf_search_filename"] = ""
#     # reader_easyocr = easyocr.Reader(['en'])
#     # lang_list = ['en']
#     # gpu = False
#     # reader_easyocr = easyocr.Reader(lang_list, gpu)
    
#     # # chrome_options = Options()
#     # chrome_options = uc.ChromeOptions()

#     # # chrome_options.headless = False
#     # chrome_options.add_argument('--headless=new')
#     # chrome_options.page_load_strategy = 'none'
#     # # options.page_load_strategy = 'eager'
#     # chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
#     # chrome_options.add_argument("--excludeSwitches=['enable-automation']")
#     # chrome_options.add_argument("--disable-popup-blocking")
#     # chrome_options.add_argument("--disable-infobars")
#     # # chrome_options.add_argument("--window-size=1280,720")
#     # # chrome_options.window_size="1280,720"
#     # # chrome_options.add_argument('--incognito') 
#     # # chrome_options.add_argument('--verbose')
#     # # chrome_options.add_argument('--no-sandbox')
#     # chrome_options.add_argument("--start-maximized")
#     # # chrome_options.add_argument('--headless')
#     # # chrome_options.add_argument("--window-size=1280,720")
#     # chrome_options.add_argument("--disable-notifications")
#     # # chrome_options.add_argument("--deny-permission-prompts")
#     # # chrome_options.add_argument("--disable-crash-reporter")
#     # # # chrome_options.add_argument("--disable-extensions")
#     # chrome_options.add_argument("--disable-in-process-stack-traces")
#     # # chrome_options.add_extention("CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx")
#     # # chrome_options.add_argument("--disable-logging")
#     # # chrome_options.add_argument("--disable-dev-shm-usage")
#     # # chrome_options.add_argument("--log-level=3")

#     # # # Exclude the collection of enable-automation switches 
#     # # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
#     # # chrome_options.add_experimental_option("useAutomationExtension", False) 
#     # chrome_options.add_experimental_option("prefs", {
#     # # "download.default_directory": r"C:\Users\l\Downloads",
#     # # "download.default_directory": "*",
#     # "download.prompt_for_download": False,
#     # "download.directory_upgrade": True,
#     # # "safebrowsing.enabled": True,
#     # "safebrowsing_for_trusted_sources_enabled": False,
#     # "safebrowsing.enabled": False,
    
#     # "credentials_enable_service": False,
#     # "profile.password_manager_enabled": False,
#     # "detach": True,
    
#     # "excludeSwitches": ["enable-automation", 'enable-logging'],
#     # 'useAutomationExtension': False,
#     # })
#     # chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
#     # chrome_options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
#     # # chrome_options.add_experimental_option('androidPackage', 'com.android.chrome')
    
#     # # prefs = {"download.default_directory" : "C:/Users/popularweb6231/python_work/"}
#     # # chrome_options.add_experimental_option("prefs", prefs)
#     # # path_to_extension = r'H:\virtual2\SELENIUM\1.54.0_1'
#     # # chrome_options.add_argument("--embedded-extension-options")
#     # # path_to_extension = r"https://chromewebstore.google.com/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm"
#     # # chrome_options.add_argument(path_to_extension)
#     # # chrome_options.add_argument('load-extension=' + path_to_extension)
#     # # chrome_options.add_extension(r'H:/virtual2/SELENIUM/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx')
#     # chrome_options.add_extension(r"D:/virtual_python_39/booksmart-app/static/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx")

#     # time.sleep(10)
#     # # driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()), )
#     # capa = DesiredCapabilities.CHROME
#     # capa["pageLoadStrategy"] = "none"
#     # # global driver
 
#     # driver = uc.Chrome(desired_capabilities=capa, options=chrome_options)
#     book_scrap.run_driver = driver
#     context_book_scrap["driver_book_scrap"] = driver
#     # driver = uc.Chrome(options=chrome_options)
#     # driver.set_window_size(1280, 720)
#     # action = ActionChains(driver)
#     time.sleep(1.4)
#     # driver.maximize_window()
#     time.sleep(1.2)
#     # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
#     # driver.execute_script("Object.defineProperty(navigator, 'uc', {get: () => undefined})") 
#     # driver.get("https://docer.pl/")

#     # driver.implicitly_wait(2)
#     print("START book_scrap")
#     try:
#         url = r"https://docer.pl/"
#         time.sleep(2.1)
#         log = ()
#         logs = [('booksmart01', 'Djangoapp01d'), ('booksmart02', 'Djangoapp02d'), ('booksmart03', 'Djangoapp03d'),('booksmart01@hotmail.com', 'Djangoapp01d'), ('booksmart02@hotmail.com', 'Djangoapp02d'), ('booksmart03@hotmail.com', 'Djangoapp03d'), ('booksmart02', 'Djangoapp02d'), ('booksmart02@hotmail.com', 'Djangoapp02d')]
#         random.shuffle(logs)
#         log = random.choice(logs)
#         print("log =", log)
#         time.sleep(1.7)
#         driver.get(url)
#     except Exception as e:
#         print(f"2. Exception as {e}")
    
#         time.sleep(12.4)
        
#     try:
#         driver.execute_script("""
#                             // window.localStorage.clear();
#                             // window.sessionStorage.clear();
                            
#                             localStorage.clear();
#                             sessionStorage.clear();
#                             """)
#     except JavascriptException:
#         print("JavascriptException Storage.clear")    
        
#     time.sleep(2.2)        
#     try:
#         btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#         if btn_cookies:
#             print("YES //button[@mode='primary']")
#             try:
#                 driver.execute_script("arguments[0].click();", btn_cookies)
#             except JavascriptException:
#                 print("1. JavascriptException btn_cookies")     
#             # driver.set_window_size(800, 600)
            
#     except NoSuchElementException:
#         print("1. NoSuchElementException btn_cookie")
#         time.sleep(1.2)
#         try:
#             btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#             if btn_cookies:
#                 print("YES //button[@mode='primary']")
#                 try:
#                     driver.execute_script("arguments[0].click();", btn_cookies)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_cookies")     
#                 # driver.set_window_size(800, 600)
                
#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_cookie")        
        
#     time.sleep(1.4)
        
#     try:
#         btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')

#         if btn_login:
#             print("btn_login")
#             try:
#                 driver.execute_script("arguments[0].click()", btn_login)
#             except JavascriptException:
#                 print("1. JavascriptException btn_login click")

#             time.sleep(1.9)
#             try:
#                 username_input = driver.find_element(By.ID, "user_email")
#                 print("1a. username_input")
#                 if username_input:
#                     print("1b. username_input")
#                     action.move_to_element(username_input)
#                     action.click(username_input)
#                     action.perform()
#                     time.sleep(0.3)
#                     username_input.send_keys(log[0])
                    
#                 time.sleep(1.4)

#                 password_input = driver.find_element(By.ID, "user_password")
#                 if password_input:
#                     action.move_to_element(password_input)
#                     time.sleep(0.5)
#                     action.click(password_input)
#                     action.perform()
#                     time.sleep(0.4)
#                     password_input.send_keys(log[1])
                    
#                 time.sleep(1.2)
                
#                 remember_input = driver.find_element(By.ID, "user_remember")
#                 if remember_input.is_selected():
                    
#                     print("checkbox is selected")
#                 else:
#                     print("checkbox is unselected")          
                        
#                 submit = driver.find_element(By.ID, "login_submit")
#                 if submit:
#                     action.move_to_element(submit)
#                     time.sleep(0.4)
#                     action.click(submit)
#                     action.perform()
#                     time.sleep(1.4)    
                                        
#             except NoSuchElementException:
#                 print("NoSuchElementException login_inputs")
#                 time.sleep(2.2)        


#     except NoSuchElementException:
#         print(f"except no such element btn_login")
#         time.sleep(2.5)
#         driver.refresh()
#         time.sleep(8.2)
        
#         try:
#             dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#             try:
#                 action.move_to_element(dissmiss_button)
#                 time.sleep(0.3)
#                 action.click(dissmiss_button)
#                 action.perform()
#             except MoveTargetOutOfBoundsException:
#                 print("MoveTargetOutOfBoundsException dissmiss-button")
            
#         except NoSuchElementException:
#             print(f"NoSuchElementException dissmiss_button")
                
#         time.sleep(3.4)
#         try:
#             btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#             if btn_cookies:
#                 print("YES //button[@mode='primary']")
#                 try:
#                     driver.execute_script("arguments[0].click();", btn_cookies)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_cookies")     
#                 # driver.set_window_size(800, 600)
                
#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_cookie")
#             time.sleep(1.2)

        
#         try:
#             btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')
#             # btn_login = WebDriverWait(driver, 5.6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body > nav.main-header.sticky > div > nav > ul > li:nth-child(2) > a')))
#             if btn_login:
#                 print("btn_login")
#                 try:
#                     driver.execute_script("arguments[0].click()", btn_login)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_login click")

#                 time.sleep(1.9)
#                 try:
#                     username_input = driver.find_element(By.ID, "user_email")
#                     print("1a. username_input")
#                     if username_input:
#                         print("1b. username_input")
#                         action.move_to_element(username_input)
#                         action.click(username_input)
#                         action.perform()
#                         time.sleep(0.3)
#                         username_input.send_keys(log[0])
                        
#                     time.sleep(1.4)

#                     password_input = driver.find_element(By.ID, "user_password")
#                     if password_input:
#                         action.move_to_element(password_input)
#                         time.sleep(0.5)
#                         action.click(password_input)
#                         action.perform()
#                         time.sleep(0.4)
#                         password_input.send_keys(log[1])
                        
#                     time.sleep(1.2)
                    
#                     remember_input = driver.find_element(By.ID, "user_remember")
#                     if remember_input.is_selected():
                        
#                         print("checkbox is selected")
#                     else:
#                         print("checkbox is unselected")          
                        
#                     submit = driver.find_element(By.ID, "login_submit")
#                     if submit:
#                         action.move_to_element(submit)
#                         time.sleep(0.4)
#                         action.click(submit)
#                         action.perform()
#                         time.sleep(1.4)    
                                            
#                 except NoSuchElementException:
#                     print("NoSuchElementException login_inputs")


#         except NoSuchElementException:
#             print("2. NoSuchElementException btn_login")
#         # except TimeoutException:
#         #     print(f"except no such element btn_login") 
#             context_book_scrap["login_pass"] = "no login pass"              
#             try:
#                 book_scrap.pdf_url_download_found = "link pdf unfinished"
#                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#             except Exception as e:
#                 print(f"serializer.save() Exception as link pdf unfinished {e}")
                
#                 # time.sleep(1.6)
#                 # driver.close()
#                 # time.sleep(1.2)
#                 # driver.quit()
#                 # time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 # return result_bot
                                         
#     time.sleep(5.6)
#     # driver.set_window_size(1024, 720)
#     try:
#         book_to_search = f'{author_book_docer}+{title_download_docer.replace(" ", "+")}'
#         print("book_to_search =", book_to_search)
#         # driver.get(f'https://docer.pl/show/?q={book_to_search}&ext=pdf')
#         url_pdfs = f'https://docer.pl/show/?q={book_to_search}&ext=pdf'
#         time.sleep(5.4)
#         # link_first = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_book_docer}")]')
#         print("urls_pdf =", url_pdfs)
#         print("author_book_docer =", author_book_docer)
#         driver.get(url_pdfs)
#     except Exception as e:
#         print(f"book_to_search Exception as {e}")
        
#     time.sleep(9.8)
        
#     try:
#         captcha_input_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#         while True:
#             captcha_input_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#             if captcha_input_1:
#                 print("1. captcha_input_1")
#                 time.sleep(4.2)
#                 captcha_img_1 = captcha_input_1.find_element(By.XPATH, "preceding-sibling::*[1]")
#                 print("captcha_img_1 src =", captcha_img_1.get_attribute("src"))

#                 try:
#                     captcha_img_1.screenshot("captcha_img_1.png")
#                     time.sleep(1.4)
#                     screenshot_captcha_1 = Image.open("captcha_img_1.png")
#                     screenshot_captcha_1.show()
#                     time.sleep(5.4)
                    
#                     result_recaptcha_1 = reader_easyocr.readtext("captcha_img_1.png", detail=0, beamWidth=1, batch_size=4)
#                     time.sleep(7.6)
                    
#                     captcha_solution_1 = result_recaptcha_1[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                     print("captcha_solution_1 =", captcha_solution_1)
                    
#                     try:
#                         action.move_to_element(captcha_input_1)
#                         time.sleep(0.2)
#                         action.click(captcha_input_1)
#                         action.perform()
#                         time.sleep(0.3)
#                         captcha_input_1.send_keys(captcha_solution_1)
                        
#                         time.sleep(4.3)
#                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                         time.sleep(0.11)
#                         action.move_to_element(captcha_submit_2)
#                         time.sleep(0.2)
#                         action.click(captcha_submit_2)
#                         action.perform()                 
#                         time.sleep(2.3)
#                         # driver.execute_script("arguments[0].click()", captcha_submit_2)
#                     except MoveTargetOutOfBoundsException:
#                         print("1. MoveTargetOutOfBoundsException captcha_1")
#                         time.sleep(2.3)   
#                         try:
#                             action.move_to_element(captcha_input_1)
#                             time.sleep(0.2)
#                             action.click(captcha_input_1)
#                             action.perform()
#                             time.sleep(0.3)
#                             captcha_input_1.send_keys(captcha_solution_1)
                            
#                             time.sleep(4.3)
#                             captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                             time.sleep(0.11)
#                             action.move_to_element(captcha_submit_2)
#                             time.sleep(0.2)
#                             action.click(captcha_submit_2)
#                             action.perform()                 
#                             time.sleep(2.3)  
#                             # driver.execute_script("arguments[0].click()", captcha_submit_2)     
#                         except MoveTargetOutOfBoundsException:
#                             print("2. MoveTargetOutOfBoundsException captcha_1")
#                             time.sleep(2.4)
#                 except ScreenshotException:
#                     print(f"2a. ScreenshotException")
#                     time.sleep(3.7)                      
                    
#                     try:
#                         captcha_input_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                         while True:
#                             captcha_input_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                             if captcha_input_1:
#                                 print("1. captcha_input_1")
#                                 time.sleep(4.2)
#                                 captcha_img_1 = captcha_input_1.find_element(By.XPATH, "preceding-sibling::*[1]")
#                                 print("captcha_img_1 src =", captcha_img_1.get_attribute("src"))

#                                 try:
#                                     captcha_img_1.screenshot("captcha_img_1.png")
#                                     time.sleep(1.4)
#                                     # screenshot_captcha_1 = Image.open("captcha_img_1.png")
#                                     # screenshot_captcha_1.show()
#                                     time.sleep(5.4)
                                    
#                                     result_recaptcha_1 = reader_easyocr.readtext("captcha_img_1.png", detail=0, beamWidth=1, batch_size=4)
#                                     time.sleep(7.6)
                                    
#                                     captcha_solution_1 = result_recaptcha_1[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                                     print("captcha_solution_1 =", captcha_solution_1)
                                    
#                                     try:
#                                         action.move_to_element(captcha_input_1)
#                                         time.sleep(0.2)
#                                         action.click(captcha_input_1)
#                                         action.perform()
#                                         time.sleep(0.3)
#                                         captcha_input_1.send_keys(captcha_solution_1)
                                        
#                                         time.sleep(4.3)
#                                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                         time.sleep(0.11)
#                                         action.move_to_element(captcha_submit_2)
#                                         time.sleep(0.2)
#                                         action.click(captcha_submit_2)
#                                         action.perform()                 
#                                         time.sleep(2.3)  
#                                         # driver.execute_script("arguments[0].click()", captcha_submit_2)
#                                     except MoveTargetOutOfBoundsException:
#                                         print("1. MoveTargetOutOfBoundsException captcha_1")
#                                         time.sleep(2.3)   
                                               
#                                     # try:
#                                     #     captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #     if captcha_submit_1:
#                                     #         print("captcha_submit_1")
#                                     #         action.move_to_element(captcha_submit_1)
#                                     #         time.sleep(0.2)
#                                     #         action.click(captcha_submit_1)
#                                     #         action.perform()                  
#                                     # except NoSuchElementException:
#                                     #     print("NoSuchElementException captcha_submit_1")
#                                     #     time.sleep(2.3) 
#                                     #     try:
#                                     #         captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #         if captcha_submit_1:
#                                     #             print("captcha_submit_1")
#                                     #             action.move_to_element(captcha_submit_1)
#                                     #             time.sleep(0.2)
#                                     #             action.click(captcha_submit_1)
#                                     #             # driver.execute_script("arguments[0].click()", captcha_submit_1)   
#                                     #             action.perform()                  
#                                     #     except NoSuchElementException:
#                                     #         print("NoSuchElementException captcha_submit_1")
                                            
#             #                     except ScreenshotException:
#             #                         print(f"2a. ScreenshotException")
#             #                         time.sleep(3.7)  
                                    
#             #                 else:
#             #                     print("1. NO captcha_1")
#             #                     continue
                            
                               
#             #         except NoSuchElementException:
#             #             print("NoSuchElementException captcha_input_1")
#             #             continue
                
#             #     continue
                                           
#             # else:
#             #     print("2. NO captcha_1")
#             #     continue    
            
#                                 except ScreenshotException:
#                                     print(f"2a. ScreenshotException")
#                                     time.sleep(3.7)  
                                                
#                                 else:
#                                     print("1. NO captcha_1")
#                                     continue    
                                    
#                             continue   

#                     except NoSuchElementException:
#                         print("except NoSuchElementException captcha_1")   
#                         continue
                        
#                 else:
#                     print("2. NO captcha_1")
#                     continue             
                
#             continue                      
                                                  
#     except NoSuchElementException:
#         print(f"except NoSuchElementException captcha_1")

#         time.sleep(2.1)
#     try:    
#         text_contains = f'//a[contains(text(), "{author_book_docer}")]'
#         print("2. text_contains =", text_contains)
#         time.sleep(0.6)
#         link_first = driver.find_element(By.XPATH, text_contains)
#         if link_first:
#             print("1. link_first")
            
#             try:
#                 file_name = link_first.text
#                 print("1. file_name =", file_name)
#                 context_book_scrap["pdf_search_filename"] = file_name
#                 book_scrap.link_first_filename = file_name
                
#                 context_book_scrap["link_first"] = "link first confirmed"                
#                 link_first_filename_serializer = book_scrap.link_first_filename                        
#                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': link_first_filename_serializer}, partial=True)
#                 if serializer.is_valid():
#                     serializer.save() 
#                     print("1. serializer.save() link first")
#             except Exception as e:
#                 print(f"1. serializer.save() link first Exception as {e}")
                
#             try:    
#                 driver.execute_script("arguments[0].click();", link_first)
#                 print("1. CLICK link first")
#                 # a.move_to_element(link_first).click().perform()
#                 # link_first.click()
#                 # action.move_to_element(link_first)
#                 # time.sleep(0.3)
#                 # action.click(link_first)
#                 # action.perform()
#                 # time.sleep(1.4)
#                 time.sleep(7.3)
#                 driver_current_url = driver.current_url
#                 context_book_scrap["driver_current_url"] = driver_current_url
#             except JavascriptException:
#                 print("1. JavascriptException CLICK link first")

    
#     except NoSuchElementException:
#         print("1. NoSuchElementException link_first")
#         time.sleep(2.1)
        
#         try:    
#             text_contains = f'//a[contains(text(), "{author_book_docer}")]'
#             print("2. text_contains =", text_contains)
#             time.sleep(0.6)
#             link_first = driver.find_element(By.XPATH, text_contains)
#             if link_first:
#                 print("2. link_first")
                
#                 try:
#                     file_name = link_first.text
#                     book_scrap.link_first_filename = file_name
#                     context_book_scrap["pdf_search_filename"] = file_name                    
#                     print("2. file_name =", file_name)
#                     context_book_scrap["link_first"] = "link first confirmed"                    
#                     link_first_filename_serializer = book_scrap.link_first_filename                        
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': link_first_filename_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save() 
#                         print("2. serializer.save() link first")
#                 except Exception as e:
#                     print(f"serializer.save() link first Exception as {e}")
                    
#                 try:    
#                     driver.execute_script("arguments[0].click();", link_first)
#                     print("2. CLICK link first")
#                 except JavascriptException:
#                     print("2. JavascriptException CLICK link first")
                    
#         except NoSuchElementException:
#             print("2 NoSuchElementException link_first")
#             try:    
#                 text_contains = f'//a[contains(text(), "{title_book_docer}")]'
#                 print("2. text_contains =", text_contains)
#                 time.sleep(0.6)
#                 link_first = driver.find_element(By.XPATH, text_contains)
#                 if link_first:
#                     print("3. link_first")
                    
#                     try:
#                         file_name = link_first.text
#                         context_book_scrap["pdf_search_filename"] = file_name
#                         book_scrap.link_first_filename = "link pdf unfinished"
#                         print("3. file_name =", file_name)
#                         context_book_scrap["link_first"] = "link first unconfirmed"
#                         link_first_filename_serializer = book_scrap.link_first_filename                        
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': link_first_filename_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save() 
#                             print("3. serializer.save() link first")
#                     except Exception as e:
#                         print(f"3. serializer.save() link first Exception as {e}")
                        
#                     try:    
#                         driver.execute_script("arguments[0].click();", link_first)
#                         print("3. CLICK link first")
#                     except JavascriptException:
#                         print("3. JavascriptException CLICK link first")    
#             except NoSuchElementException:
#                 print("2 NoSuchElementException link_first")
#                 try:
                    
#                     book_scrap.link_first_filename = "no pdf filename docer"
#                     print("4. book_scrap.link_first_filename =", book_scrap.link_first_filename)
                    
#                     link_first_filename_serializer = book_scrap.link_first_filename                        
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'pdf_search_filename': link_first_filename_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save() 
#                         print("4. serializer.save() link first")
#                 except Exception as e:
#                     print(f"4. serializer.save() link first Exception as {e}")
                    
#                 time.sleep(1.6)
#                 driver.close()
#                 time.sleep(1.2)
#                 driver.quit()
#                 time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"517 kill_chrome Exception as {e}")
                
#                 print("1. END book_scrap")    
#                 return result_bot                

#     time.sleep(8.9) 
#     # driver.set_window_size(800, 600)

#     driver_current_url = context_book_scrap["driver_current_url"]
#     print("733 driver_current_url =", driver_current_url)
#     try:
#         print("1. def url_exists(driver_current_url, context_book_scrap_url_exist, book_pdf_bot):")
#         url_exists(driver_current_url, context_book_scrap_url_exist, book_pdf_bot)
#         time.sleep(1.1)
#         print('1. context_book_scrap_url_exist["link_first"] =', context_book_scrap_url_exist["link_first"])
#         if context_book_scrap_url_exist["link_first"] != "link first confirmed":
#             context_book_scrap.update(context_book_scrap_url_exist)
#             time.sleep(1.6)
#             driver.close()
#             time.sleep(1.2)
#             driver.quit()       
#             return result_bot
#         else:
#             print('1. context_book_scrap_url_exists ["link_first"] =', context_book_scrap_url_exist ["link_first"])                      
            
#     except Exception as e:
#         print(f"1. url_exists Exception as {e}")    

#     time.sleep(1.6)      
   
#     try:
#         captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#         while True:
#             captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#             if captcha_input_2:
#                 print("1. captcha_input_2")
#                 time.sleep(12.2)
#                 captcha_img_2 = captcha_input_2.find_element(By.XPATH, "preceding-sibling::*[1]")
#                 print("captcha_img_2 src =", captcha_img_2.get_attribute("src"))

#                 try:
#                     captcha_img_2.screenshot("captcha_img_2.png")
#                     time.sleep(1.4)
#                     # screenshot_captcha_2 = Image.open("captcha_img_2.png")
#                     # screenshot_captcha_2.show()
#                     time.sleep(5.4)
                    
#                     result_recaptcha_2 = reader_easyocr.readtext("captcha_img_2.png", detail=0, beamWidth=1, batch_size=4)
#                     time.sleep(7.6)
                    
#                     captcha_solution_2 = result_recaptcha_2[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                     print("captcha_solution_2 =", captcha_solution_2)
                    
#                     try:
#                         action.move_to_element(captcha_input_2)
#                         time.sleep(0.2)
#                         action.click(captcha_input_2)
#                         action.perform()
#                         time.sleep(0.3)
#                         captcha_input_2.send_keys(captcha_solution_2)
                        
#                         time.sleep(4.3)
#                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                         time.sleep(0.11)
#                         action.move_to_element(captcha_submit_2)
#                         time.sleep(0.2)
#                         action.click(captcha_submit_2)
#                         action.perform()                 
#                         time.sleep(2.3)  
#                         # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                     except MoveTargetOutOfBoundsException:
#                         print("1. MoveTargetOutOfBoundsException captcha_2")
#                         time.sleep(2.3)
#                         try:
#                             action.move_to_element(captcha_input_2)
#                             time.sleep(0.2)
#                             action.click(captcha_input_2)
#                             action.perform()
#                             time.sleep(0.3)
#                             captcha_input_2.send_keys(captcha_solution_2)
                            
#                             time.sleep(4.3)
#                             captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                             time.sleep(0.11)
#                             action.move_to_element(captcha_submit_2)
#                             time.sleep(0.2)
#                             action.click(captcha_submit_2)
#                             action.perform()                 
#                             time.sleep(2.3)  
#                             # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                         except MoveTargetOutOfBoundsException:
#                             print("2. MoveTargetOutOfBoundsException captcha_2")
#                             time.sleep(2.4)                        
#                 except ScreenshotException:
#                     print(f"2a. ScreenshotException")
#                     time.sleep(3.7)                        
                    
#                     try:
#                         captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                         while True:
#                             captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                             if captcha_input_2:
#                                 print("1. captcha_input_2")
#                                 time.sleep(12.2)
#                                 captcha_img_2 = captcha_input_2.find_element(By.XPATH, "preceding-sibling::*[1]")
#                                 print("captcha_img_2 src =", captcha_img_2.get_attribute("src"))

#                                 try:
#                                     captcha_img_2.screenshot("captcha_img_2.png")
#                                     time.sleep(1.4)
#                                     # screenshot_captcha_2 = Image.open("captcha_img_2.png")
#                                     # screenshot_captcha_2.show()
#                                     time.sleep(5.4)
                                    
#                                     result_recaptcha_2 = reader_easyocr.readtext("captcha_img_2.png", detail=0, beamWidth=1, batch_size=4)
#                                     time.sleep(7.6)
                                    
#                                     captcha_solution_2 = result_recaptcha_2[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                                     print("captcha_solution_2 =", captcha_solution_2)
                                    
#                                     try:
#                                         action.move_to_element(captcha_input_2)
#                                         time.sleep(0.2)
#                                         action.click(captcha_input_2)
#                                         action.perform()
#                                         time.sleep(0.3)
#                                         captcha_input_2.send_keys(captcha_solution_2)
                                        
#                                         time.sleep(4.3)
#                                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                         time.sleep(0.11)
#                                         action.move_to_element(captcha_submit_2)
#                                         time.sleep(0.2)
#                                         action.click(captcha_submit_2)
#                                         action.perform()                 
#                                         time.sleep(2.3)  
#                                         # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                                     except MoveTargetOutOfBoundsException:
#                                         print("1. MoveTargetOutOfBoundsException captcha_2") 
#                                         time.sleep(2.4)  
                                        
#                                     # try:
#                                     #     captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #     if captcha_submit_1:
#                                     #         print("captcha_submit_1")
#                                     #         action.move_to_element(captcha_submit_1)
#                                     #         time.sleep(0.2)
#                                     #         action.click(captcha_submit_1)
#                                     #         action.perform()                  
#                                     # except NoSuchElementException:
#                                     #     print("NoSuchElementException captcha_submit_1")
#                                     #     time.sleep(2.3) 
#                                     #     try:
#                                     #         captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #         if captcha_submit_1:
#                                     #             print("captcha_submit_1")
#                                     #             action.move_to_element(captcha_submit_1)
#                                     #             time.sleep(0.2)
#                                     #             action.click(captcha_submit_1)
#                                     #             # driver.execute_script("arguments[0].click()", captcha_submit_1)   
#                                     #             action.perform()                  
#                                     #     except NoSuchElementException:
#                                     #         print("NoSuchElementException captcha_submit_1")
                                                                              
#                                 except ScreenshotException:
#                                     print(f"2a. ScreenshotException")
#                                     time.sleep(3.7)  
                                                
#                                 else:
#                                     print("1. NO captcha_2")
#                                     continue    
                                    
#                             continue   

#                     except NoSuchElementException:
#                         print("except NoSuchElementException captcha_2")   
#                         continue
                        
#                 else:
#                     print("2. NO captcha_2")
#                     continue             
                
#             continue 
        
#     except NoSuchElementException:
#         print(f"except NoSuchElementException captcha_2")
            
#     time.sleep(2.1)
#     try:
#         driver.execute_script("window.scrollBy(0, 200);")
#     except JavascriptException:
#         print("1. JavascriptException window.scrollBy")
        
#     time.sleep(2.9) 
#     if context_book_scrap["login_pass"] != "no login pass":
#         try:
#             btn_download = driver.find_element(By.ID, "dwn_btn")
#             # btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
#             # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
#             if btn_download:
#                 print("1. btn_download")
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         try:
#                             driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                         except JavascriptException:
#                             print("1. JavascriptException scrollBy")
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                                        
#                 # try:
#                 #     driver.execute_script("window.scrollBy(0, window.innerHeight-800)")
#                 #     # driver.execute_script("window.scrollBy(0, 290);")
#                 # except JavascriptException:
#                 #     print("1. JavascriptException scrollBy")     
                
#                 try:
#                     driver_current_url = driver.current_url
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.get_current_url = driver_current_url
#                         print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                         get_current_url_serializer = book_scrap.get_current_url
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.get_current_url = "link pdf unconfirmed"
#                         print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                         get_current_url_serializer = book_scrap.get_current_url
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                 except Exception as e:
#                     print(f"1.url_pdf_search Exception as {e}")
#                 time.sleep(2.1)
#                 try:    
#                     action.move_to_element(btn_download)
#                     action.perform()
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException btn_download")
                    
#                 try:    
#                     driver.execute_script("arguments[0].click()", btn_download)
#                     time.sleep(12.4)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_download click")
#                     time.sleep(3.6)
#                     try:
#                         btn_download = driver.find_element(By.ID, "dwn_btn")
#                         # btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
#                         # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
#                         if btn_download:
#                             print("2. btn_download")
#                             try:    
#                                 driver.execute_script("arguments[0].click()", btn_download)
#                                 time.sleep(11.6)
#                             except JavascriptException:
#                                 print("1. JavascriptException btn_download click")
#                     except NoSuchElementException:
#                         print("3. NoSuchElementException btn_driver")
                                                    
#                 # action.release()
                
#                 time.sleep(1.3)
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         print("1. watch_header")
#                         try: 
#                             action.move_to_element(watch_header)
#                             action.perform()
#                         except MoveTargetOutOfBoundsException:
#                             print("MoveTargetOutOfBoundsException")   
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")

#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_download")              
#             time.sleep(1.4)
#             try:
#                 btn_download = driver.find_element(By.ID, "dwn_btn") 
#                 if btn_download:
#                     print("3. btn_download")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
#                         try:
#                             watch_header = driver.find_element(By.ID, "watch-header")
#                             if watch_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")                
#                     try:
#                         driver_current_url = driver.current_url
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.get_current_url = driver_current_url
#                             print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                             get_current_url_serializer = book_scrap.get_current_url
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.get_current_url = "link pdf unconfirmed"
#                             print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                             get_current_url_serializer = book_scrap.get_current_url
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                     except Exception as e:
#                         print(f"1.url_pdf_search Exception as {e}")
                           
#                     time.sleep(1.3)    
#                     try:
#                         print("2. def url_exists(driver_current_url, context_book_scrap, book_pdf_bot):")
#                         url_exists(driver_current_url, context_book_scrap_url_exist, book_pdf_bot)
#                         time.sleep(1.1)
#                         print('2. context_book_scrap_url_exist["link_first"] =', context_book_scrap_url_exist["link_first"])
#                         if context_book_scrap_url_exist["link_first"] != "link first confirmed":
#                             context_book_scrap.update(context_book_scrap_url_exist)
#                             time.sleep(1.6)
#                             driver.close()
#                             time.sleep(1.2)
#                             driver.quit()       
#                             return result_bot   
#                         else:
#                             print('2. context_book_scrap_url_exists ["link_first"] =', context_book_scrap_url_exist ["link_first"])                                                
                            
#                     except Exception as e:
#                         print(f"2. url_exists Exception as {e}")    

#                     time.sleep(1.6)      
#                     print('2. url_exists context_book_scrap["link_first"] =', context_book_scrap["link_first"])                              
                        
#                     time.sleep(1.9)
#                     try:    
#                         action.move_to_element(btn_download)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException btn_download")
                        
#                     try:    
#                         driver.execute_script("arguments[0].click()", btn_download)
#                         time.sleep(11.7)
#                     except JavascriptException:
#                         print("1. JavascriptException btn_download click")
#                         time.sleep(0.7)
#                         try:    
#                             driver.execute_script("arguments[0].click()", btn_download)
#                             time.sleep(12.8)
#                         except JavascriptException:
#                             print("1. JavascriptException btn_download click")
                                        
#                     # action.release()
#                     time.sleep(1.3)

#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             print("2. watch_header")
#                             try: 
#                                 action.move_to_element(watch_header)
#                                 action.perform()
#                             except MoveTargetOutOfBoundsException:
#                                 print("MoveTargetOutOfBoundsException")   
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")

#                     # driver.set_window_size(1024, 720)
         
#             except NoSuchElementException:
#                 print("2. NoSuchElementException btn_download")
#                 time.sleep(1.7)
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     time.sleep(2.2)
#                     driver.quit()
#                     time.sleep(2.2)

#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver.quit") 
                
#                 print("3. END book_scrap")
#                 return result_bot 
                
#         try:
#             driver.execute_script("window.open()")
#             # driver.execute_script("window.open()")
#             # driver.switch_to.window(driver.window_handles[1])
#             time.sleep(1.2)
#             driver.switch_to.window(driver.window_handles[1])
#             driver.get("chrome://downloads/")
#             time.sleep(3.4)
#             try:
#                 downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                 if downloaded_book:
#                     try:
#                         download_book_get_attribute = downloaded_book.get_attribute("href")
#                         # context_book_scrap["link_first"]
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             context_book_scrap["pdf_link"] = "link pdf confirmed"
#                             book_scrap.pdf_url_download_found = download_book_get_attribute
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()  
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             context_book_scrap["pdf_link"] = "link pdf unconfirmed"
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()         
#                     except Exception as e:
#                         print(f"serializer.save url_pdf Exception as {e}")
                    
#                     # try:
#                     #     show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                     #     # show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                     #     try:
#                     #         show_title_path = show_book_my.get_attribute("title")
#                     #         context_book_scrap["show_title_path"] = show_title_path
#                     #     except NoSuchAttributeException:
#                     #         print("1. NoSuchAttributeException show_title_path")
                            
#                     #     driver.execute_script("arguments[0].click()", show_book_my)
#                     # except JavascriptException:
#                     #     print("JavascriptException show_book_my") 
                        
#                     file_name_found = downloaded_book.text
#                     print("file_name_found =", file_name_found)
#                     # if file_name_found[:len(file_name)] == file_name:
#                     if file_name in file_name_found:
#                         pdf_url_download = book_scrap.pdf_url_download_found
                        
#                         print(f'1. pdf_url_download = {pdf_url_download}')
#                         print("SUCCESS !!! " * 5)
#                         # driver.execute_script("arguments[0].click()", downloaded_book)
#                         time.sleep(4.6)
                        
#                         try:
#                             show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                             if show_book:
#                                 print("1. show_book.text =", show_book.text)
#                                 try:
#                                     show_title_path = show_book.get_attribute("title")
#                                     if show_title_path:
#                                         print("1. show_title_path =", show_title_path)
#                                         context_book_scrap["show_title_path"] = show_title_path
#                                 except NoSuchAttributeException:
#                                     print("1. NoSuchAttributeException show_title_path")
                                    
#                                 try:
#                                     driver.execute_script("arguments[0].click()", show_book)
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         time.sleep(1.2)
#                                         driver.close()
#                                         time.sleep(2.2)
#                                         driver.quit()
                                        
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
                                        
#                                 except JavascriptException:
#                                     print("1. JavascriptException show_book")
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         time.sleep(1.2)
#                                         driver.close()
#                                         time.sleep(2.2)
#                                         driver.quit()
                                        
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
                                        


#                         except NoSuchElementException:
#                             print(f"NoSuchElementException show_book") 
#                             time.sleep(2.6)
#                             try:
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 time.sleep(1.2)

#                             except NoSuchDriverException:
#                                 print("1. NoSuchDriverException switch_to")
#                                 time.sleep(2.2)
#                                 # driver.quit()
                                
#             # except NoSuchShadowRootException:
#             #     print("1. NoSuchShadowRootException downloaded_book")
#             except JavascriptException:
#                 print("1a. JavascriptException")
                
#                 try:
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.pdf_url_download_found = "link pdf exist"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()    
#                 except Exception as e:
#                     print(f"2. link pdf exist Exception as {e}")
#                 try:
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(1.2)
                         
#                 except NoSuchDriverException:
#                     print("1. NoSuchDriverException switch_to")
#                     time.sleep(2.2)
#                     # driver.quit() 
                    
#         except JavascriptException:
#             print("1a. window.open()")
            
#             try:
#                 if context_book_scrap["link_first"] == "link first confirmed":
#                     book_scrap.pdf_url_download_found = "link pdf exist"
#                     pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                 else:
#                     book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                     pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()                    
                            
#             except Exception as e:
#                 print(f"2. link pdf exist Exception as {e}")
#             try:
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#                 time.sleep(1.2)
                         
#             except NoSuchDriverException:
#                 print("1. NoSuchDriverException switch_to")
#                 time.sleep(2.2)
#                 # driver.quit() 
                
#         try:
#             print('1. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#             file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#             if file_exist:
#                 print("1. file_exist")
#                 print("1. SUCCESS !!! " * 10)
#                 try:
#                     print("1. result_bot")
#                     # time.sleep(2.6)
#                     # driver.close()
#                     # driver.switch_to.window(driver.window_handles[0])
#                     # time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()
#                     # print("4. END book_scrap")
#                     return result_bot 
#                 except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                     print(f"1. RequestException, NewConnectionError = {err}")
#                     print("4e. END book_scrap")
#                     return result_bot

#             else:
#                 print("1. no book in folder")
#                 context_book_scrap["book_in_folder"] = "no book in folder"
#                 time.sleep(4.3)                

#         except Exception as e:
#             print(f"1. except file_exist: Exception as {e}")   
                     
#         # try:
#         #     home = os.path.expanduser("~")
#         #     downloadspath=os.path.join(home, "Downloads")
#         #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#         #     latest_file = max(list_of_files, key=os.path.getctime)
#         #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#         #     name_last_file = latest_file.split("\\")[-1][:-4]
#         #     if name_last_file[:len(file_name)+1] == file_name:
#         #         print("SUCCESS !!! " * 10)
#         #         try:
#         #             print("1. last driver quit")
#         #             time.sleep(2.6)
#         #             driver.close()
#         #             driver.switch_to.window(driver.window_handles[0])
#         #             time.sleep(1.2)
#         #             driver.close()
#         #             time.sleep(2.2)
#         #             driver.quit()
#         #             print("4. END book_scrap")
#         #             return result_bot 
#         #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #             print(f"1. RequestException, NewConnectionError = {err}")
#         #             print("4e. END book_scrap")
#         #             return result_bot

#         #     else:
#         #         print("1. no book in folder")
#         #         context_book_scrap["book_in_folder"] = "no book in folder"
#         #         time.sleep(4.3)
#         #         # try:
#         #         #     time.sleep(2.6)
#         #         #     driver.close()
#         #         #     driver.switch_to.window(driver.window_handles[0])

#         #         # except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #         #     print(f"1. RequestException, NewConnectionError = {err}")                
                
#         # except Exception as e:
#         #     print(f"1130. except file exist: Exception as {e}")
#         #     time.sleep(2.3)
#         #     # driver.switch_to.window(driver.window_handles[0])
               
#     elif context_book_scrap["login_pass"] == "no login pass":          
#             # time.sleep(4.6) 
#         try:
#             dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#             try:
#                 action.move_to_element(dissmiss_button)
#                 time.sleep(0.3)
#                 action.click(dissmiss_button)
#                 action.perform()
#             except MoveTargetOutOfBoundsException:
#                 print("MoveTargetOutOfBoundsException dissmiss-button")
#                 try:
#                     dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                     try:
#                         action.move_to_element(dissmiss_button)
#                         time.sleep(0.3)
#                         action.click(dissmiss_button)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException dissmiss-button")
                    
#                 except NoSuchElementException:
#                     print(f"NoSuchElementException dissmiss_button")                
            
#         except NoSuchElementException:
#             print(f"NoSuchElementException dissmiss_button")
                
#         time.sleep(3.4)            
#         try:
#             div_captcha = driver.find_element(By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-border")
#             if div_captcha:
#                 try:
#                     action.move_to_element(div_captcha)
#                     action.click(div_captcha)
#                     action.perform()
#                     time.sleep(1.3)
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException")
                    
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         print("3. watch_header")
#                         try: 
#                             action.move_to_element(watch_header)
#                             action.perform()
#                         except MoveTargetOutOfBoundsException:
#                             print("MoveTargetOutOfBoundsException")   
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             print("4. watch_header")
#                             try: 
#                                 action.move_to_element(watch_header)
#                                 action.perform()
#                             except MoveTargetOutOfBoundsException:
#                                 print("MoveTargetOutOfBoundsException")   
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")

#         except NoSuchElementException:
#             print("NoSuchElementException div_captcha")    
        
#         time.sleep(2.4)                      
#         try:
#             element_link_end = driver.find_element(By.ID, "iframe2")
#             if element_link_end:
#                 element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                 print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                 link_end = element_link_end.get_attribute('data-pdf-url')
#                 if link_end != None:
#                     print('1. link_end =', link_end)
#                     time.sleep(2.6)
#                     try:
#                         iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                         if iframe2_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                        
#                     time.sleep(2.9)
#                     driver.get(link_end)
#                     context_book_scrap["link_end"] = "yes link_end"
                    
#         except NoSuchElementException:
#             print("NoSuchElementException iframe2")                       

#             time.sleep(4.3)
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
                    
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"

#             except NoSuchElementException:
#                 print("1. NoSuchElementException link_end")
#                 context_book_scrap["link_end"] = "no link_end"
#                 time.sleep(1.6)
#                 # driver.close()
#                 # time.sleep(1.2)
#                 # driver.quit()
#                 # time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 print("5. END book_scrap")
#                 return result_bot             
                            
#         time.sleep(14.2)
#         if context_book_scrap["link_end"] == "yes link_end":        
#             try:
#                 driver.execute_script("window.open()")
#                 # driver.execute_script("window.open()")
#                 # driver.switch_to.window(driver.window_handles[1])
#                 time.sleep(1.2)
#                 driver.switch_to.window(driver.window_handles[1])
#                 driver.get("chrome://downloads/")
#                 time.sleep(3.4)
#                 try:
#                     downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                     if downloaded_book:
#                         try:
#                             download_book_get_attribute = downloaded_book.get_attribute("href")
#                             # context_book_scrap["link_first"]
#                             if context_book_scrap["link_first"] == "link first confirmed":
#                                 context_book_scrap["pdf_link"] = "link pdf confirmed"
#                                 book_scrap.pdf_url_download_found = download_book_get_attribute
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()  
#                             else:
#                                 book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                                 context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()         
#                         except Exception as e:
#                             print(f"serializer.save url_pdf Exception as {e}")
                        
#                         # try:
#                         #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                         #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                         #     driver.execute_script("arguments[0].click()", show_book_my)
#                         # except JavascriptException:
#                         #     print("JavascriptException show_book_my") 
                            
#                         file_name_found = downloaded_book.text
#                         print("file_name_found =", file_name_found)
#                         # if file_name_found[:len(file_name)] == file_name:
#                         if file_name in file_name_found:
#                             pdf_url_download = book_scrap.pdf_url_download_found
                            
#                             print(f'1. pdf_url_download = {pdf_url_download}')
#                             print("SUCCESS !!! " * 5)
#                             # driver.execute_script("arguments[0].click()", downloaded_book)
#                             time.sleep(4.6)
                            
#                             try:
#                                 show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                                 if show_book:
#                                     print("2. show_book.text =", show_book.text)
#                                     try:
#                                         show_title_path = show_book.get_attribute("title")
#                                         if show_title_path:
#                                             print("2. show_title_path =", show_title_path)
#                                             context_book_scrap["show_title_path"] = show_title_path
#                                     except NoSuchAttributeException:
#                                         print("2. NoSuchAttributeException show_title_path")
                                        
#                                     try:
#                                         driver.execute_script("arguments[0].click()", show_book)
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
                                            
#                                     except JavascriptException:
#                                         print("1. JavascriptException show_book")
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             # driver.close()
#                                             # time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)


#                             except NoSuchElementException:
#                                 print(f"NoSuchElementException show_book") 
#                                 time.sleep(2.6)
#                                 try:
#                                     driver.close()
#                                     driver.switch_to.window(driver.window_handles[0])
#                                     # time.sleep(1.2)
#                                     # driver.close()
#                                     # time.sleep(2.2)
#                                     # driver.quit()                            
#                                 except NoSuchDriverException:
#                                     print("1. NoSuchDriverException switch_to")

#                 except JavascriptException:
#                     print("2a. JavascriptException")
                    
#                     try:
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.pdf_url_download_found = "link pdf exist"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()    
#                     except Exception as e:
#                         print(f"2. link pdf exist Exception as {e}")
#                     try:
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()                            
#                     except NoSuchDriverException:
#                         print("1. NoSuchDriverException switch_to")
#                         time.sleep(2.2)
#                         # driver.quit()                                
                            
#                         # time.sleep(1.6)
#                         # driver.close()
#                         # time.sleep(1.2)
#                         # driver.quit()
#                         # time.sleep(2.3)
#                         # try:
#                         #     driver = book_scrap.run_driver
#                         #     kill_chrome(get_pid(driver))
#                         # except Exception as e:
#                         #     print(f"332 kill_chrome Exception as {e}")
                        
                                                
#             except Exception as e:
#                 print(f"window.open() Exception as {e}")
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(6.4)
#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver..window_handles[0]")

#             try:
#                 print('2. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#                 file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#                 if file_exist:
#                     print("2. file_exist")
#                     print("2. SUCCESS !!! " * 10)
#                     try:
#                         print("2. result_bot ")
#                         time.sleep(2.6)
#                         # driver.close()
#                         # driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()
#                         print("6. END book_scrap")
#                         return result_bot 
#                     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                         print(f"1. RequestException, NewConnectionError = {err}")
#                         print("6e. END book_scrap")
#                         return result_bot

#                 else:
#                     print("2. no book in folder")
#                     context_book_scrap["book_in_folder"] = "no book in folder"
#                     time.sleep(4.3)                

#             except Exception as e:
#                 print(f"2. except file_exist: Exception as {e}")
                                       
#             # try:
#             #     home = os.path.expanduser("~")
#             #     downloadspath=os.path.join(home, "Downloads")
#             #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#             #     latest_file = max(list_of_files, key=os.path.getctime)
#             #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#             #     name_last_file = latest_file.split("\\")[-1][:-4]
#             #     if name_last_file[:len(file_name)+1] == file_name:
#             #         print("SUCCESS !!! " * 10)
#             #         try:
#             #             print("2. last driver quit")
#             #             time.sleep(2.6)
#             #             driver.close()
#             #             driver.switch_to.window(driver.window_handles[0])
#             #             time.sleep(1.2)
#             #             driver.close()
#             #             time.sleep(2.2)
#             #             driver.quit()
#             #             print("6. END book_scrap")
#             #             return result_bot 
                    
#             #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#             #             print(f"2. RequestException, NewConnectionError = {err}")   
#             #             print("6e. END book_scrap")
#             #             return result_bot                                         

#             #     else:
#             #         print("2. no book in folder")
#             #         context_book_scrap["book_in_folder"] = "no book in folder"
                    
#             # except Exception as e:
#             #     print(f"1402 except file exist: Exception as {e}")
                    
#         elif context_book_scrap["link_end"] == "yes link_end":            
                        
#             try:
#                 dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                 try:
#                     action.move_to_element(dissmiss_button)
#                     time.sleep(0.3)
#                     action.click(dissmiss_button)
#                     action.perform()
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException dissmiss-button")
                
#             except NoSuchElementException:
#                 print(f"NoSuchElementException dissmiss_button")  
#                 time.sleep(2.1)
#                 try:
#                     dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                     try:
#                         action.move_to_element(dissmiss_button)
#                         time.sleep(0.3)
#                         action.click(dissmiss_button)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException dissmiss-button")
                    
#                 except NoSuchElementException:
#                     print(f"NoSuchElementException dissmiss_button") 
                                        
#             time.sleep(2.6)              
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"
#             except NoSuchElementException:
#                 print("NoSuchElementException iframe2")                       

#                 time.sleep(4.3)
#                 try:
#                     element_link_end = driver.find_element(By.ID, "iframe2")
#                     if element_link_end:
#                         element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                         print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                         link_end = element_link_end.get_attribute('data-pdf-url')
                        
#                         if link_end != None:
#                             print('1. link_end =', link_end)
#                             time.sleep(2.6)
#                             try:
#                                 iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                                 if iframe2_header:
#                                     try:
#                                         driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                     except JavascriptException:
#                                         print("1. JavascriptException scrollBy")
#                             except NoSuchElementException:
#                                 print("NoSuchElementException watch_header")
                                
#                             time.sleep(2.9)
#                             driver.get(link_end)
#                             context_book_scrap["link_end"] = "yes link_end"

#                 except NoSuchElementException:
#                     print("1. NoSuchElementException link_end")            
                
#                     try:
#                         time.sleep(2.6)
#                         driver.close()
#                         time.sleep(2.2)
#                         driver.quit()
#                         time.sleep(2.2)
#                         print("7. END book_scrap")
#                         return result_bot 
                    
#                     except NoSuchDriverException:
#                         print("NoSuchDriverException driver.quit")  
                        
#     if context_book_scrap["link_end"] == "yes link_end":                    
#         try:
#             driver.execute_script("window.open()")
#             # driver.execute_script("window.open()")
#             # driver.switch_to.window(driver.window_handles[1])
#             time.sleep(1.2)
#             driver.switch_to.window(driver.window_handles[1])
#             driver.get("chrome://downloads/")
#             time.sleep(3.4)
#             try:
#                 downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                 if downloaded_book:
#                     try:
#                         download_book_get_attribute = downloaded_book.get_attribute("href")
#                         # context_book_scrap["link_first"]
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             context_book_scrap["pdf_link"] = "link pdf confirmed"
#                             book_scrap.pdf_url_download_found = download_book_get_attribute
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()  
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()         
#                     except Exception as e:
#                         print(f"serializer.save url_pdf Exception as {e}")
                    
#                     # try:
#                     #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                     #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                     #     driver.execute_script("arguments[0].click()", show_book_my)
#                     # except JavascriptException:
#                     #     print("JavascriptException show_book_my") 
                        
#                     file_name_found = downloaded_book.text
#                     print("file_name_found =", file_name_found)
#                     # if file_name_found[:len(file_name)] == file_name:
#                     if file_name in file_name_found:
#                         pdf_url_download = book_scrap.pdf_url_download_found
                        
#                         print(f'1. pdf_url_download = {pdf_url_download}')
#                         print("SUCCESS !!! " * 5)
#                         # driver.execute_script("arguments[0].click()", downloaded_book)
#                         time.sleep(4.6)
                        
#                         try:
#                             show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                             if show_book:
#                                 print("3. show_book.text =", show_book.text)
#                                 try:
#                                     show_title_path = show_book.get_attribute("title")
#                                     if show_title_path:
#                                         print("3. show_title_path =", show_title_path)
#                                         context_book_scrap["show_title_path"] = show_title_path
#                                 except NoSuchAttributeException:
#                                     print("3. NoSuchAttributeException show_title_path")
                                    
#                                 try:
#                                     driver.execute_script("arguments[0].click()", show_book)
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         time.sleep(1.2)
#                                         driver.close()
#                                         time.sleep(2.2)
#                                         driver.quit()
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
#                                         # driver.quit()
#                                 except JavascriptException:
#                                     print("1. JavascriptException show_book")
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         # time.sleep(1.2)
#                                         # driver.close()
#                                         # time.sleep(2.2)
#                                         # driver.quit()
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
#                                         # driver.quit()


#                         except NoSuchElementException:
#                             print(f"NoSuchElementException show_book") 
#                             time.sleep(2.6)
#                             try:
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 time.sleep(1.2)
                          
#                             except NoSuchDriverException:
#                                 print("1. NoSuchDriverException switch_to")
#                                 # time.sleep(2.2)
#                                 # driver.quit()


#             # except NoSuchShadowRootException:
#             #     print("1. NoSuchShadowRootException downloaded_book")
#             except JavascriptException:
#                 print("3a. JavascriptException")
                
#                 try:
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.pdf_url_download_found = "link pdf exist"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()    
#                 except Exception as e:
#                     print(f"2. link pdf exist Exception as {e}")
#                 try:
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()                            
#                 except NoSuchDriverException:
#                     print("1. NoSuchDriverException switch_to")
#                     time.sleep(2.2)
#                     # driver.quit()                                
                        
#                     # time.sleep(1.6)
#                     # driver.close()
#                     # time.sleep(1.2)
#                     # driver.quit()
#                     # time.sleep(2.3)
#                     # try:
#                     #     driver = book_scrap.run_driver
#                     #     kill_chrome(get_pid(driver))
#                     # except Exception as e:
#                     #     print(f"332 kill_chrome Exception as {e}")
                    
                                            
#         except Exception as e:
#             print(f"window.open() Exception as {e}")
#             try:
#                 time.sleep(2.6)
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#                 time.sleep(6.4)
#             except NoSuchDriverException:
#                 print("NoSuchDriverException driver..window_handles[0]")            
#             # try:
#             #     driver = book_scrap.run_driver
#             #     kill_chrome(get_pid(driver))
#             # except Exception as e:
#             #     print(f"332 kill_chrome Exception as {e}")            
#         try:
#             print('3. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#             file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#             if file_exist:
#                 print("3. file_exist")
#                 print("3. SUCCESS !!! " * 10)
#                 try:
#                     print("3. result_bot")
#                     time.sleep(2.6)
#                     # driver.close()
#                     # driver.switch_to.window(driver.window_handles[0])
#                     # time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()
#                     print("3_4. END book_scrap")
#                     return result_bot 
#                 except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                     print(f"3. RequestException, NewConnectionError = {err}")
#                     print("3_4e. END book_scrap")
#                     return result_bot

#             else:
#                 print("3. no book in folder")
#                 context_book_scrap["book_in_folder"] = "no book in folder"
#                 time.sleep(4.3)                

#         except Exception as e:
#             print(f"3. except file_exist: Exception as {e}") 
                            
#         # try:
#         #     home = os.path.expanduser("~")
#         #     downloadspath=os.path.join(home, "Downloads")
#         #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#         #     latest_file = max(list_of_files, key=os.path.getctime)
#         #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#         #     name_last_file = latest_file.split("\\")[-1][:-4]
#         #     if name_last_file[:len(file_name)+1] == file_name:
#         #         print("SUCCESS !!! " * 10)
                
#         #         try:
#         #             print("3. book in folder")
#         #             context_book_scrap["book_in_folder"] = "book in folder"
#         #             time.sleep(2.6)
#         #             driver.close()
#         #             driver.switch_to.window(driver.window_handles[0])
#         #             time.sleep(1.2)
#         #             driver.close()
#         #             time.sleep(2.2)
#         #             driver.quit()
#         #             return result_bot
#         #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #             print(f"3. RequestException, NewConnectionError = {err}")
#         #             return result_bot
#         #     else:
#         #         print("3. no book in folder")
#         #         context_book_scrap["book_in_folder"] = "no book in folder"
#         #         time.sleep(4.3)
                
#         # except Exception as e:
#         #     print(f"except file exist: Exception as {e}") 

    
#     elif context_book_scrap["link_end"] != "yes link_end" or context_book_scrap["book_in_folder"] != "book in folder": 
                
#         try:
#             element_link_end = driver.find_element(By.ID, "iframe2")
#             if element_link_end:
#                 element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                 print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                 link_end = element_link_end.get_attribute('data-pdf-url')
#                 if link_end != None:
#                     print('1. link_end =', link_end)
#                     time.sleep(2.6)
#                     try:
#                         iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                         if iframe2_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                        
#                     time.sleep(2.9)
#                     driver.get(link_end)
#                     context_book_scrap["link_end"] = "yes link_end"
                    
#         except NoSuchElementException:
#             print("NoSuchElementException iframe2")                       

#             time.sleep(4.3)
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
                    
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"

#             except NoSuchElementException:
#                 print("1. NoSuchElementException link_end")
#                 context_book_scrap["link_end"] = "no link_end"
#                 time.sleep(1.6)
#                 driver.close()
#                 time.sleep(1.2)
#                 driver.quit()
#                 time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 print("5. END book_scrap")
#                 return result_bot             
                            
#         time.sleep(14.2)
#         if context_book_scrap["link_end"] == "yes link_end":        
#             try:
#                 driver.execute_script("window.open()")
#                 # driver.execute_script("window.open()")
#                 # driver.switch_to.window(driver.window_handles[1])
#                 time.sleep(1.2)
#                 driver.switch_to.window(driver.window_handles[1])
#                 driver.get("chrome://downloads/")
#                 time.sleep(3.4)
#                 try:
#                     downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                     if downloaded_book:
#                         try:
#                             download_book_get_attribute = downloaded_book.get_attribute("href")
#                             # context_book_scrap["link_first"]
#                             if context_book_scrap["link_first"] == "link first confirmed":
#                                 context_book_scrap["pdf_link"] = "link pdf confirmed"
#                                 book_scrap.pdf_url_download_found = download_book_get_attribute
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()  
#                             else:
#                                 book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                                 context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()         
#                         except Exception as e:
#                             print(f"serializer.save url_pdf Exception as {e}")
                        
#                         # try:
#                         #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                         #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                         #     driver.execute_script("arguments[0].click()", show_book_my)
#                         # except JavascriptException:
#                         #     print("JavascriptException show_book_my") 
                            
#                         file_name_found = downloaded_book.text
#                         print("file_name_found =", file_name_found)
#                         # if file_name_found[:len(file_name)] == file_name:
#                         if file_name in file_name_found:
#                             pdf_url_download = book_scrap.pdf_url_download_found
                            
#                             print(f'1. pdf_url_download = {pdf_url_download}')
#                             print("SUCCESS !!! " * 5)
#                             # driver.execute_script("arguments[0].click()", downloaded_book)
#                             time.sleep(4.6)
                            
#                             try:
#                                 show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                                 if show_book:
#                                     print("4. show_book.text =", show_book.text)
#                                     try:
#                                         show_title_path = show_book.get_attribute("title")
#                                         if show_title_path:
#                                             print("4. show_title_path =", show_title_path)
#                                             context_book_scrap["show_title_path"] = show_title_path
#                                     except NoSuchAttributeException:
#                                         print("4. NoSuchAttributeException show_title_path")
                                        
#                                     try:
#                                         driver.execute_script("arguments[0].click()", show_book)
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                     except JavascriptException:
#                                         print("1. JavascriptException show_book")
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             driver.quit()


#                             except NoSuchElementException:
#                                 print(f"NoSuchElementException show_book") 
#                                 time.sleep(2.6)
#                                 try:
#                                     driver.close()
#                                     driver.switch_to.window(driver.window_handles[0])
#                                     # time.sleep(1.2)
#                                     # driver.close()
#                                     # time.sleep(2.2)
#                                     # driver.quit()                            
#                                 except NoSuchDriverException:
#                                     print("1. NoSuchDriverException switch_to")

#                 except JavascriptException:
#                     print("2a. JavascriptException")
                    
#                     try:
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.pdf_url_download_found = "link pdf exist"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()    
#                     except Exception as e:
#                         print(f"2. link pdf exist Exception as {e}")
#                     try:
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()                            
#                     except NoSuchDriverException:
#                         print("1. NoSuchDriverException switch_to")
#                         time.sleep(2.2)
#                         # driver.quit()                                
                            
#                         # time.sleep(1.6)
#                         # driver.close()
#                         # time.sleep(1.2)
#                         # driver.quit()
#                         # time.sleep(2.3)
#                         # try:
#                         #     driver = book_scrap.run_driver
#                         #     kill_chrome(get_pid(driver))
#                         # except Exception as e:
#                         #     print(f"332 kill_chrome Exception as {e}")
                        
                                                
#             except Exception as e:
#                 print(f"window.open() Exception as {e}")
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(6.4)
#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver..window_handles[0]")
                    
#             try:
#                 print('4. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#                 file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#                 if file_exist:
#                     print("4. file_exist")
#                     print("4. SUCCESS !!! " * 10)
#                     try:
#                         print("4. result_bot")
#                         time.sleep(2.6)
#                         # driver.close()
#                         # driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()
#                         print("4_4. END book_scrap")
#                         return result_bot 
#                     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                         print(f"4. RequestException, NewConnectionError = {err}")
#                         print("4_4e. END book_scrap")
#                         return result_bot

#                 else:
#                     print("3. no book in folder")
#                     context_book_scrap["book_in_folder"] = "no book in folder"
#                     time.sleep(4.3)                

#             except Exception as e:
#                 print(f"3. except file_exist: Exception as {e}")  
                                     
#             # try:
#             #     home = os.path.expanduser("~")
#             #     downloadspath=os.path.join(home, "Downloads")
#             #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#             #     latest_file = max(list_of_files, key=os.path.getctime)
#             #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#             #     name_last_file = latest_file.split("\\")[-1][:-4]
#             #     if name_last_file[:len(file_name)+1] == file_name:
#             #         print("SUCCESS !!! " * 10)
#             #         try:
#             #             print("2. last driver quit")
#             #             time.sleep(2.6)
#             #             driver.close()
#             #             driver.switch_to.window(driver.window_handles[0])
#             #             time.sleep(1.2)
#             #             driver.close()
#             #             time.sleep(2.2)
#             #             driver.quit()
#             #             print("6. END book_scrap")
#             #             return result_bot 
                    
#             #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#             #             print(f"2. RequestException, NewConnectionError = {err}")  
#             #             return result_bot                 

#             #     else:
#             #         print("2. no book in folder")
#             #         context_book_scrap["book_in_folder"] = "no book in folder"
                    
#             # except Exception as e:
#             #     print(f"1402 except file exist: Exception as {e}")
        
#     try:
#         print("2050. last driver quit")
#         if driver.service.is_connectable() == True:
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])
#             time.sleep(1.2)
#             driver.close()
#             time.sleep(2.2)
#             driver.quit()
#             return result_bot
#         else:
#             return result_bot
#     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         print(f"RequestException, NewConnectionError = {err}")  
#         return result_bot
    
#     # import httplib, socket

#     # try:
#     #     driver.quit()
#     # except httplib.CannotSendRequest:
#     #     print "Driver did not terminate"
#     # except socket.error:
#     #     print "Driver did not terminate"
#     # else:
#     #     print "Driver terminated"

#     # try:
#     #     time.sleep(1.6)
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)
#     #     try:
#     #         driver = book_scrap.run_driver
#     #         kill_chrome(get_pid(driver))
#     #     except Exception as e:
#     #         print(f"332 kill_chrome Exception as {e}")
#     #         # os.system('cmd /k "taskkill /F /IM chrome.exe /T"')
#     # except NoSuchDriverException:
#     #     print("NoSuchDriverException")
#     # try:
#     #     driver.execute_script("window.close()")
#     # except JavascriptException:
#     #     print("avascriptException")
#     # time.sleep(1.6)
#     # try:
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)
#     # except NoSuchDriverException:
#     #     print("NoSuchDriverException driver.quit")
        
#     # try:
#     #     driver.get("https://www.bing.com/")
#     #     time.sleep(2.4)
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)     
#     # except Exception as e:
#     #     print(f"bing Exception as {e}")   
        
#     print("8. END book_scrap")  
      
#     return result_bot   

# def book_scrap_ready(book_id_book_scrap_ready, driver, action, reader_easyocr, *args, **kwargs):
#     print("def book_scrap_ready")
#     result_bot = "result bot"
#     context_book_scrap = {}
#     context_book_scrap_url_exist = {}
#     book_pdf_bot = Book.objects.filter(pk=book_id_book_scrap_ready).first()
#     book_pdf_bot_values = Book.objects.filter(pk=book_id_book_scrap_ready).values()[0]
#     book_scrap_ready.pdf_url_download_found = book_pdf_bot_values["url_pdf"]
#     url_page_pdf = book_pdf_bot_values["url_pdf_search"]
#     pdf_search_filename = book_pdf_bot_values["pdf_search_filename"]
#     driver_current_url = url_page_pdf
#     context_book_scrap["login_pass"] = ""
#     context_book_scrap["driver_current_url"] = ""
#     context_book_scrap["link_end"] = "no link_end" 
#     context_book_scrap["link_first"] = "link first confirmed"
#     context_book_scrap["show_title_path"] = ""
    
#     # chrome_options = Options()
    
#     # lang_list = ['en']
#     # gpu = False
#     # reader_easyocr = easyocr.Reader(lang_list, gpu)
#     # # reader_easyocr = easyocr.Reader(['en'])
#     # chrome_options = uc.ChromeOptions()

#     # chrome_options.headless = False
#     # chrome_options.page_load_strategy = 'none'
#     # # options.page_load_strategy = 'eager'
#     # chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
#     # chrome_options.add_argument("--excludeSwitches=['enable-automation']")
#     # chrome_options.add_argument("--disable-popup-blocking")
#     # chrome_options.add_argument("--disable-infobars")
#     # # chrome_options.add_argument('--incognito') 

#     # chrome_options.add_argument("--disable-notifications")

#     # chrome_options.add_argument("--disable-in-process-stack-traces")

#     # chrome_options.add_experimental_option("prefs", {
#     # "download.default_directory": r"C:\Users\l\downloads",
#     # # "download.default_directory": "C:\Users\BONUM\Downloads\",
#     # # "download.default_directory": r"C:\Users\BONUM\Downloads",
#     # "download.prompt_for_download": False,
#     # "download.directory_upgrade": True,
#     # # "safebrowsing.enabled": True,
#     # "safebrowsing_for_trusted_sources_enabled": False,
#     # "safebrowsing.enabled": False
#     # })
#     # chrome_options.add_extension(r"D:/virtual_python_39/booksmart-app/static/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx")
#     # time.sleep(10)
#     # # driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()), )
#     # capa = DesiredCapabilities.CHROME
#     # capa["pageLoadStrategy"] = "none"
#     # # global driver
 
#     # driver = uc.Chrome(desired_capabilities=capa, options=chrome_options)
#     # book_scrap_ready.run_driver = driver
#     # # driver = uc.Chrome(options=chrome_options)
#     # # driver.set_window_size(1280, 720)
#     # action = ActionChains(driver)
#     # time.sleep(1.4)
#     # driver.maximize_window()
#     # time.sleep(1.2)
#     # # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
#     # driver.execute_script("Object.defineProperty(navigator, 'uc', {get: () => undefined})") 
#     # # driver.get("https://docer.pl/")

#     # # driver.implicitly_wait(2)
#     print("START book_scrap_ready")
#     try:
#         url = r"https://docer.pl/"
#         time.sleep(2.1)
#         log = ()
#         logs = [('booksmart01', 'Djangoapp01d'), ('booksmart02', 'Djangoapp02d'), ('booksmart03', 'Djangoapp03d'),('booksmart01@hotmail.com', 'Djangoapp01d'), ('booksmart02@hotmail.com', 'Djangoapp02d'), ('booksmart03@hotmail.com', 'Djangoapp03d'), ('booksmart02', 'Djangoapp02d'), ('booksmart02@hotmail.com', 'Djangoapp02d')]
#         random.shuffle(logs)
#         log = random.choice(logs)
#         print("log =", log)
#         time.sleep(1.7)
#         driver.get(url)
#     except Exception as e:
#         print(f"2. Exception as {e}")
    
#         time.sleep(12.4)
        
#     try:
#         driver.execute_script("""
#                             // window.localStorage.clear();
#                             // window.sessionStorage.clear();
                            
#                             localStorage.clear();
#                             sessionStorage.clear();
#                             """)
#     except JavascriptException:
#         print("JavascriptException Storage.clear")    
        
#     time.sleep(2.2)        
#     try:
#         btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#         if btn_cookies:
#             print("YES //button[@mode='primary']")
#             try:
#                 driver.execute_script("arguments[0].click();", btn_cookies)
#             except JavascriptException:
#                 print("1. JavascriptException btn_cookies")     
#             # driver.set_window_size(800, 600)
            
#     except NoSuchElementException:
#         print("1. NoSuchElementException btn_cookie")
#         time.sleep(1.2)
#         try:
#             btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#             if btn_cookies:
#                 print("YES //button[@mode='primary']")
#                 try:
#                     driver.execute_script("arguments[0].click();", btn_cookies)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_cookies")     
#                 # driver.set_window_size(800, 600)
                
#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_cookie")        
        
#     time.sleep(1.4)
        
#     try:
#         btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')

#         if btn_login:
#             print("btn_login")
#             try:
#                 driver.execute_script("arguments[0].click()", btn_login)
#             except JavascriptException:
#                 print("1. JavascriptException btn_login click")

#             time.sleep(1.9)
#             try:
#                 username_input = driver.find_element(By.ID, "user_email")
#                 print("1a. username_input")
#                 if username_input:
#                     print("1b. username_input")
#                     action.move_to_element(username_input)
#                     action.click(username_input)
#                     action.perform()
#                     time.sleep(0.3)
#                     username_input.send_keys(log[0])
                    
#                 time.sleep(1.4)

#                 password_input = driver.find_element(By.ID, "user_password")
#                 if password_input:
#                     action.move_to_element(password_input)
#                     time.sleep(0.5)
#                     action.click(password_input)
#                     action.perform()
#                     time.sleep(0.4)
#                     password_input.send_keys(log[1])
                    
#                 time.sleep(1.2)
                
#                 remember_input = driver.find_element(By.ID, "user_remember")
#                 if remember_input.is_selected():
                    
#                     print("checkbox is selected")
#                 else:
#                     print("checkbox is unselected")          
                        
#                 submit = driver.find_element(By.ID, "login_submit")
#                 if submit:
#                     action.move_to_element(submit)
#                     time.sleep(0.4)
#                     action.click(submit)
#                     action.perform()
#                     time.sleep(1.4)    
                                        
#             except NoSuchElementException:
#                 print("NoSuchElementException login_inputs")
#                 time.sleep(2.2)        


#     except NoSuchElementException:
#         print(f"except no such element btn_login")
#         time.sleep(2.5)
#         driver.refresh()
#         time.sleep(8.2)
        
#         try:
#             dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#             try:
#                 action.move_to_element(dissmiss_button)
#                 time.sleep(0.3)
#                 action.click(dissmiss_button)
#                 action.perform()
#             except MoveTargetOutOfBoundsException:
#                 print("MoveTargetOutOfBoundsException dissmiss-button")
            
#         except NoSuchElementException:
#             print(f"NoSuchElementException dissmiss_button")
                
#         time.sleep(3.4)
#         try:
#             btn_cookies = driver.find_element(By.XPATH, "//button[@mode='primary']")
#             if btn_cookies:
#                 print("YES //button[@mode='primary']")
#                 try:
#                     driver.execute_script("arguments[0].click();", btn_cookies)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_cookies")     
#                 # driver.set_window_size(800, 600)
                
#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_cookie")
#             time.sleep(1.2)

        
#         try:
#             btn_login = driver.find_element(By.CSS_SELECTOR, '.login_show_btn')
#             # btn_login = WebDriverWait(driver, 5.6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#body > nav.main-header.sticky > div > nav > ul > li:nth-child(2) > a')))
#             if btn_login:
#                 print("btn_login")
#                 try:
#                     driver.execute_script("arguments[0].click()", btn_login)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_login click")

#                 time.sleep(1.9)
#                 try:
#                     username_input = driver.find_element(By.ID, "user_email")
#                     print("1a. username_input")
#                     if username_input:
#                         print("1b. username_input")
#                         action.move_to_element(username_input)
#                         action.click(username_input)
#                         action.perform()
#                         time.sleep(0.3)
#                         username_input.send_keys(log[0])
                        
#                     time.sleep(1.4)

#                     password_input = driver.find_element(By.ID, "user_password")
#                     if password_input:
#                         action.move_to_element(password_input)
#                         time.sleep(0.5)
#                         action.click(password_input)
#                         action.perform()
#                         time.sleep(0.4)
#                         password_input.send_keys(log[1])
                        
#                     time.sleep(1.2)
                    
#                     remember_input = driver.find_element(By.ID, "user_remember")
#                     if remember_input.is_selected():
                        
#                         print("checkbox is selected")
#                     else:
#                         print("checkbox is unselected")          
                        
#                     submit = driver.find_element(By.ID, "login_submit")
#                     if submit:
#                         action.move_to_element(submit)
#                         time.sleep(0.4)
#                         action.click(submit)
#                         action.perform()
#                         time.sleep(1.4)    
                                            
#                 except NoSuchElementException:
#                     print("NoSuchElementException login_inputs")


#         except NoSuchElementException:
#             print("2. NoSuchElementException btn_login")
#         # except TimeoutException:
#         #     print(f"except no such element btn_login") 
#             context_book_scrap["login_pass"] = "no login pass"              
#             try:
#                 book_scrap.pdf_url_download_found = "link pdf unfinished"
#                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                 if serializer.is_valid():
#                     serializer.save()
#             except Exception as e:
#                 print(f"serializer.save() Exception as link pdf unfinished {e}")
                
#                 # time.sleep(1.6)
#                 # driver.close()
#                 # time.sleep(1.2)
#                 # driver.quit()
#                 # time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 # return result_bot

#     time.sleep(4.6) 
#     try:   
#         driver.get(url_page_pdf)
#     except Exception as e:
#         print(f"1639 exception; {e}")
      
#     try:
#         captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#         while True:
#             captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#             if captcha_input_2:
#                 print("1. captcha_input_2")
#                 time.sleep(12.2)
#                 captcha_img_2 = captcha_input_2.find_element(By.XPATH, "preceding-sibling::*[1]")
#                 print("captcha_img_2 src =", captcha_img_2.get_attribute("src"))

#                 try:
#                     captcha_img_2.screenshot("captcha_img_2.png")
#                     time.sleep(1.4)
#                     # screenshot_captcha_2 = Image.open("captcha_img_2.png")
#                     # screenshot_captcha_2.show()
#                     time.sleep(5.4)
                    
#                     result_recaptcha_2 = reader_easyocr.readtext("captcha_img_2.png", detail=0, beamWidth=1, batch_size=4)
#                     time.sleep(7.6)
                    
#                     captcha_solution_2 = result_recaptcha_2[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                     print("captcha_solution_2 =", captcha_solution_2)
                    
#                     try:
#                         action.move_to_element(captcha_input_2)
#                         time.sleep(0.2)
#                         action.click(captcha_input_2)
#                         action.perform()
#                         time.sleep(0.3)
#                         captcha_input_2.send_keys(captcha_solution_2)
                        
#                         time.sleep(4.3)
#                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                         time.sleep(0.11)
#                         action.move_to_element(captcha_submit_2)
#                         time.sleep(0.2)
#                         action.click(captcha_submit_2)
#                         action.perform()                 
#                         time.sleep(2.3)  
#                         # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                     except MoveTargetOutOfBoundsException:
#                         print("1. MoveTargetOutOfBoundsException captcha_2")
#                         time.sleep(2.3)
#                         try:
#                             action.move_to_element(captcha_input_2)
#                             time.sleep(0.2)
#                             action.click(captcha_input_2)
#                             action.perform()
#                             time.sleep(0.3)
#                             captcha_input_2.send_keys(captcha_solution_2)
                            
#                             time.sleep(4.3)
#                             captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                             time.sleep(0.11)
#                             action.move_to_element(captcha_submit_2)
#                             time.sleep(0.2)
#                             action.click(captcha_submit_2)
#                             action.perform()                 
#                             time.sleep(2.3)  
#                             # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                         except MoveTargetOutOfBoundsException:
#                             print("2. MoveTargetOutOfBoundsException captcha_2")
#                             time.sleep(2.4)                        
#                 except ScreenshotException:
#                     print(f"2a. ScreenshotException")
#                     time.sleep(3.7)                        
                    
#                     try:
#                         captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                         while True:
#                             captcha_input_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.text-class")
#                             if captcha_input_2:
#                                 print("1. captcha_input_2")
#                                 time.sleep(12.2)
#                                 captcha_img_2 = captcha_input_2.find_element(By.XPATH, "preceding-sibling::*[1]")
#                                 print("captcha_img_2 src =", captcha_img_2.get_attribute("src"))

#                                 try:
#                                     captcha_img_2.screenshot("captcha_img_2.png")
#                                     time.sleep(1.4)
#                                     # screenshot_captcha_2 = Image.open("captcha_img_2.png")
#                                     # screenshot_captcha_2.show()
#                                     time.sleep(5.4)
                                    
#                                     result_recaptcha_2 = reader_easyocr.readtext("captcha_img_2.png", detail=0, beamWidth=1, batch_size=4)
#                                     time.sleep(7.6)
                                    
#                                     captcha_solution_2 = result_recaptcha_2[0].replace(" ", "").replace("tt", 'H').replace(")", "j").replace("FF", "A").replace("ff", "A").replace("2", "z").replace("#", "h").replace("0", "O").lower() #.replace("v", "u")
#                                     print("captcha_solution_2 =", captcha_solution_2)
                                    
#                                     try:
#                                         action.move_to_element(captcha_input_2)
#                                         time.sleep(0.2)
#                                         action.click(captcha_input_2)
#                                         action.perform()
#                                         time.sleep(0.3)
#                                         captcha_input_2.send_keys(captcha_solution_2)
                                        
#                                         time.sleep(4.3)
#                                         captcha_submit_2 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                         time.sleep(0.11)
#                                         action.move_to_element(captcha_submit_2)
#                                         time.sleep(0.2)
#                                         action.click(captcha_submit_2)
#                                         action.perform()                 
#                                         time.sleep(2.3)  
#                                         # driver.execute_script("arguments[0].click()", captcha_submit_2)   
#                                     except MoveTargetOutOfBoundsException:
#                                         print("1. MoveTargetOutOfBoundsException captcha_2") 
#                                         time.sleep(2.4)  
                                        
#                                     # try:
#                                     #     captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #     if captcha_submit_1:
#                                     #         print("captcha_submit_1")
#                                     #         action.move_to_element(captcha_submit_1)
#                                     #         time.sleep(0.2)
#                                     #         action.click(captcha_submit_1)
#                                     #         action.perform()                  
#                                     # except NoSuchElementException:
#                                     #     print("NoSuchElementException captcha_submit_1")
#                                     #     time.sleep(2.3) 
#                                     #     try:
#                                     #         captcha_submit_1 = driver.find_element(By.CSS_SELECTOR, "#eow-title > center > div > form > input.myButton2")
#                                     #         if captcha_submit_1:
#                                     #             print("captcha_submit_1")
#                                     #             action.move_to_element(captcha_submit_1)
#                                     #             time.sleep(0.2)
#                                     #             action.click(captcha_submit_1)
#                                     #             # driver.execute_script("arguments[0].click()", captcha_submit_1)   
#                                     #             action.perform()                  
#                                     #     except NoSuchElementException:
#                                     #         print("NoSuchElementException captcha_submit_1")
                                                                              
#                                 except ScreenshotException:
#                                     print(f"2a. ScreenshotException")
#                                     time.sleep(3.7)  
                                                
#                                 else:
#                                     print("1. NO captcha_2")
#                                     continue    
                                    
#                             continue   

#                     except NoSuchElementException:
#                         print("except NoSuchElementException captcha_2")   
#                         continue
                        
#                 else:
#                     print("2. NO captcha_2")
#                     continue             
                
#             continue 
        
#     except NoSuchElementException:
#         print(f"except NoSuchElementException captcha_2")
            
#     time.sleep(2.1)
#     try:
#         driver.execute_script("window.scrollBy(0, 200);")
#     except JavascriptException:
#         print("1. JavascriptException window.scrollBy")
        
#     time.sleep(2.9) 
#     if context_book_scrap["login_pass"] != "no login pass":
#         try:
#             btn_download = driver.find_element(By.ID, "dwn_btn")
#             # btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
#             # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
#             if btn_download:
#                 print("1. btn_download")
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         try:
#                             driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                         except JavascriptException:
#                             print("1. JavascriptException scrollBy")
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                                        
#                 # try:
#                 #     driver.execute_script("window.scrollBy(0, window.innerHeight-800)")
#                 #     # driver.execute_script("window.scrollBy(0, 290);")
#                 # except JavascriptException:
#                 #     print("1. JavascriptException scrollBy")     
                
#                 try:
#                     driver_current_url = driver.current_url
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.get_current_url = driver_current_url
#                         print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                         get_current_url_serializer = book_scrap.get_current_url
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.get_current_url = "link pdf unconfirmed"
#                         print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                         get_current_url_serializer = book_scrap.get_current_url
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                 except Exception as e:
#                     print(f"1.url_pdf_search Exception as {e}")
#                 time.sleep(2.1)
#                 try:    
#                     action.move_to_element(btn_download)
#                     action.perform()
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException btn_download")
                    
#                 try:    
#                     driver.execute_script("arguments[0].click()", btn_download)
#                     time.sleep(10.4)
#                 except JavascriptException:
#                     print("1. JavascriptException btn_download click")
#                     time.sleep(3.6)
#                     try:
#                         btn_download = driver.find_element(By.ID, "dwn_btn")
#                         # btn_download = WebDriverWait(driver, 12.4).until(EC.visibility_of_element_located((By.ID, "dwn_btn")))
#                         # btn_download = WebDriverWait(driver, 5.1).until(EC.element_to_be_clickable((By.ID, "dwn_btn")))
#                         if btn_download:
#                             print("2. btn_download")
#                             try:    
#                                 driver.execute_script("arguments[0].click()", btn_download)
#                                 time.sleep(11.3)
#                             except JavascriptException:
#                                 print("1. JavascriptException btn_download click")
#                     except NoSuchElementException:
#                         print("3. NoSuchElementException btn_driver")
                                                    
#                 # action.release()
                
#                 time.sleep(1.3)
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         print("1. watch_header")
#                         try: 
#                             action.move_to_element(watch_header)
#                             action.perform()
#                         except MoveTargetOutOfBoundsException:
#                             print("MoveTargetOutOfBoundsException")   
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")

#         except NoSuchElementException:
#             print("1. NoSuchElementException btn_download")              
#             time.sleep(1.4)
#             try:
#                 btn_download = driver.find_element(By.ID, "dwn_btn") 
#                 if btn_download:
#                     print("3. btn_download")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
#                         try:
#                             watch_header = driver.find_element(By.ID, "watch-header")
#                             if watch_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", watch_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")                
#                     try:
#                         driver_current_url = driver.current_url
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.get_current_url = driver_current_url
#                             print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                             get_current_url_serializer = book_scrap.get_current_url
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.get_current_url = "link pdf unconfirmed"
#                             print("1. book_scrap.get_current_url =", book_scrap.get_current_url)                
#                             get_current_url_serializer = book_scrap.get_current_url
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf_search': get_current_url_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                     except Exception as e:
#                         print(f"1.url_pdf_search Exception as {e}")
                           
#                     time.sleep(1.3)    
#                     try:
#                         print("2. def url_exists(driver_current_url, context_book_scrap, book_pdf_bot):")

#                         print("2840 driver_current_url =", driver_current_url)
#                         url_exists(driver_current_url, context_book_scrap_url_exist, book_pdf_bot)
#                         time.sleep(1.1)
#                         print('2. context_book_scrap_url_exist["link_first"] =', context_book_scrap_url_exist["link_first"])
#                         if context_book_scrap_url_exist["link_first"] != "link first confirmed":
#                             context_book_scrap.update(context_book_scrap_url_exist)
#                             time.sleep(1.6)
#                             driver.close()
#                             time.sleep(1.2)
#                             driver.quit()       
#                             return result_bot   
#                         else:
#                             print('2. context_book_scrap_url_exists ["link_first"] =', context_book_scrap_url_exist ["link_first"])                                                
                            
#                     except Exception as e:
#                         print(f"2. url_exists Exception as {e}")    

#                     time.sleep(1.6)      
#                     print('2. url_exists context_book_scrap["link_first"] =', context_book_scrap["link_first"])                              
                        
#                     time.sleep(1.9)
#                     try:    
#                         action.move_to_element(btn_download)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException btn_download")
                        
#                     try:    
#                         driver.execute_script("arguments[0].click()", btn_download)
#                         time.sleep(11.9)
#                     except JavascriptException:
#                         print("1. JavascriptException btn_download click")
#                         time.sleep(0.7)
#                         try:    
#                             driver.execute_script("arguments[0].click()", btn_download)
#                             time.sleep(12.6)
#                         except JavascriptException:
#                             print("1. JavascriptException btn_download click")
                                        
#                     # action.release()
#                     time.sleep(1.3)

#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             print("2. watch_header")
#                             try: 
#                                 action.move_to_element(watch_header)
#                                 action.perform()
#                             except MoveTargetOutOfBoundsException:
#                                 print("MoveTargetOutOfBoundsException")   
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")

#                     # driver.set_window_size(1024, 720)
         
#             except NoSuchElementException:
#                 print("2. NoSuchElementException btn_download")
#                 time.sleep(1.7)
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     time.sleep(2.2)
#                     driver.quit()
#                     time.sleep(2.2)

#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver.quit") 
                
#                 print("3. END book_scrap")
#                 return result_bot 
                
#         try:
#             driver.execute_script("window.open()")
#             # driver.execute_script("window.open()")
#             # driver.switch_to.window(driver.window_handles[1])
#             time.sleep(1.2)
#             driver.switch_to.window(driver.window_handles[1])
#             driver.get("chrome://downloads/")
#             time.sleep(3.4)
#             try:
#                 downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                 if downloaded_book:
#                     try:
#                         download_book_get_attribute = downloaded_book.get_attribute("href")
#                         # context_book_scrap["link_first"]
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             context_book_scrap["pdf_link"] = "link pdf confirmed"
#                             book_scrap.pdf_url_download_found = download_book_get_attribute
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()  
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()         
#                     except Exception as e:
#                         print(f"serializer.save url_pdf Exception as {e}")
                    
#                     # try:
#                     #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                     #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                     #     driver.execute_script("arguments[0].click()", show_book_my)
#                     # except JavascriptException:
#                     #     print("JavascriptException show_book_my") 
                        
#                     file_name_found = downloaded_book.text
#                     print("file_name_found =", file_name_found)
#                     # if file_name_found[:len(file_name)] == file_name:
#                     if pdf_search_filename in file_name_found:
#                         pdf_url_download = book_scrap.pdf_url_download_found
                        
#                         print(f'1. pdf_url_download = {pdf_url_download}')
#                         print("SUCCESS !!! " * 5)
#                         # driver.execute_script("arguments[0].click()", downloaded_book)
#                         time.sleep(4.6)
                        
#                         try:
#                             show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                             if show_book:
#                                 print("1a. show_book.text =", show_book.text)
#                                 # try:
#                                 try:
#                                     show_title_path = show_book.get_attribute("title")
#                                     if show_title_path:
#                                         print("1a. show_title_path =", show_title_path)
#                                         context_book_scrap["show_title_path"] = show_title_path
#                                 except NoSuchAttributeException:
#                                     print("1. NoSuchAttributeException show_title_path")
                                        
#                                 driver.execute_script("arguments[0].click()", show_book)
#                                 time.sleep(2.6)
#                                 try:
#                                     driver.close()
#                                     driver.switch_to.window(driver.window_handles[0])
#                                     time.sleep(1.2)
#                                     driver.close()
#                                     time.sleep(2.2)
#                                     driver.quit()
#                                 except NoSuchDriverException:
#                                     print("1. NoSuchDriverException switch_to")
#                                 #     time.sleep(2.2)
#                                 #     driver.close()
#                                 #     driver.switch_to.window(driver.window_handles[0])
#                                 # except JavascriptException:
#                                 #     print("1. JavascriptException show_book")
#                                 #     time.sleep(2.6)
#                                 #     try:
#                                 #         driver.close()
#                                 #         driver.switch_to.window(driver.window_handles[0])
#                                 #         time.sleep(1.2)
#                                 #         # driver.close()
#                                 #         # time.sleep(2.2)
#                                 #         # driver.quit()
#                                 #     except NoSuchDriverException:
#                                 #         print("1. NoSuchDriverException switch_to")
#                                 #         time.sleep(2.2)
#                                 #         driver.close()
#                                 #         driver.switch_to.window(driver.window_handles[0])


#                         except NoSuchElementException:
#                             print(f"NoSuchElementException show_book") 
#                             time.sleep(2.6)
#                             try:
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 time.sleep(1.2)
#                                 # driver.close()
#                                 # time.sleep(2.2)
#                                 # driver.quit()                            
#                             except NoSuchDriverException:
#                                 print("1. NoSuchDriverException switch_to")
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
                                
#             # except NoSuchShadowRootException:
#             #     print("1. NoSuchShadowRootException downloaded_book")
#             except JavascriptException:
#                 print("1a. JavascriptException")
                
#                 try:
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.pdf_url_download_found = "link pdf exist"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()    
#                 except Exception as e:
#                     print(f"2. link pdf exist Exception as {e}")
#                 try:
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(1.2)
                         
#                 except NoSuchDriverException:
#                     print("1. NoSuchDriverException switch_to")
#                     time.sleep(2.2)
#                     # driver.close()
#                     # driver.switch_to.window(driver.window_handles[0])
                    
#         except JavascriptException:
#             print("1a. window.open()")
            
#             try:
#                 if context_book_scrap["link_first"] == "link first confirmed":
#                     book_scrap.pdf_url_download_found = "link pdf exist"
#                     pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()
#                 else:
#                     book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                     pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                     serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                     if serializer.is_valid():
#                         serializer.save()                    
                            
#             except Exception as e:
#                 print(f"2. link pdf exist Exception as {e}")
#             try:
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#                 time.sleep(1.2)
                         
#             except NoSuchDriverException:
#                 print("1. NoSuchDriverException switch_to")
#                 # driver.close()
#                 # driver.switch_to.window(driver.window_handles[0])
#                 # driver.quit()
#         try:
#             print('1a. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#             file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#             if file_exist:
#                 print("1a. file_exist")
#                 print("1a. SUCCESS !!! " * 10)
#                 try:
#                     print("1a. result_bot")
#                     time.sleep(2.6)
#                     # driver.close()
#                     # driver.switch_to.window(driver.window_handles[0])
#                     # time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()
#                     print("1a_4. END book_scrap")
#                     return result_bot 
#                 except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                     print(f"3. RequestException, NewConnectionError = {err}")
#                     print("1a_4e. END book_scrap")
#                     return result_bot

#             else:
#                 print("3. no book in folder")
#                 context_book_scrap["book_in_folder"] = "no book in folder"
#                 time.sleep(4.3)                

#         except Exception as e:
#             print(f"3. except file_exist: Exception as {e}")  
                                 
#         # try:
#         #     home = os.path.expanduser("~")
#         #     downloadspath=os.path.join(home, "Downloads")
#         #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#         #     latest_file = max(list_of_files, key=os.path.getctime, default=0)
#         #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#         #     name_last_file = latest_file.split("\\")[-1][:-4]
#         #     if name_last_file[:len(pdf_search_filename)+1] == pdf_search_filename:
#         #         print("SUCCESS !!! " * 10)
#         #         try:
#         #             print("1. last driver quit")
#         #             time.sleep(2.6)
#         #             driver.close()
#         #             driver.switch_to.window(driver.window_handles[0])
#         #             time.sleep(1.2)
#         #             driver.close()
#         #             time.sleep(2.2)
#         #             driver.quit()
#         #             return result_bot 
#         #             print("4. END book_scrap")
#         #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #             print(f"1. RequestException, NewConnectionError = {err}")                    
#         #             print("4e. END book_scrap")
#         #             return result_bot
        
#         #     else:
#         #         print("1. no book in folder")
#         #         context_book_scrap["book_in_folder"] = "no book in folder"
#         #         time.sleep(4.3)
#         #         try:
#         #             time.sleep(2.6)
#         #             driver.close()
#         #             driver.switch_to.window(driver.window_handles[0])

#         #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #             print(f"1. RequestException, NewConnectionError = {err}")                
                
#         # except Exception as e:
#         #     print(f"1130. except file exist: Exception as {e}")
#         #     time.sleep(2.3)
#         #     # driver.close()
#         #     # driver.switch_to.window(driver.window_handles[0])
               
#     elif context_book_scrap["login_pass"] == "no login pass":          
#             # time.sleep(4.6) 
#         try:
#             dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#             try:
#                 action.move_to_element(dissmiss_button)
#                 time.sleep(0.3)
#                 action.click(dissmiss_button)
#                 action.perform()
#             except MoveTargetOutOfBoundsException:
#                 print("MoveTargetOutOfBoundsException dissmiss-button")
#                 try:
#                     dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                     try:
#                         action.move_to_element(dissmiss_button)
#                         time.sleep(0.3)
#                         action.click(dissmiss_button)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException dissmiss-button")
                    
#                 except NoSuchElementException:
#                     print(f"NoSuchElementException dissmiss_button")                
            
#         except NoSuchElementException:
#             print(f"NoSuchElementException dissmiss_button")
                
#         time.sleep(3.4)            
#         try:
#             div_captcha = driver.find_element(By.CSS_SELECTOR, "#recaptcha-anchor > div.recaptcha-checkbox-border")
#             if div_captcha:
#                 try:
#                     action.move_to_element(div_captcha)
#                     action.click(div_captcha)
#                     action.perform()
#                     time.sleep(1.3)
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException")
                    
#                 try:
#                     watch_header = driver.find_element(By.ID, "watch-header")
#                     if watch_header:
#                         print("3. watch_header")
#                         try: 
#                             action.move_to_element(watch_header)
#                             action.perform()
#                         except MoveTargetOutOfBoundsException:
#                             print("MoveTargetOutOfBoundsException")   
#                 except NoSuchElementException:
#                     print("NoSuchElementException watch_header")
#                     try:
#                         watch_header = driver.find_element(By.ID, "watch-header")
#                         if watch_header:
#                             print("4. watch_header")
#                             try: 
#                                 action.move_to_element(watch_header)
#                                 action.perform()
#                             except MoveTargetOutOfBoundsException:
#                                 print("MoveTargetOutOfBoundsException")   
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")

#         except NoSuchElementException:
#             print("NoSuchElementException div_captcha")    
        
#         time.sleep(2.4)                      
#         try:
#             element_link_end = driver.find_element(By.ID, "iframe2")
#             if element_link_end:
#                 element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                 print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                 link_end = element_link_end.get_attribute('data-pdf-url')
#                 if link_end != None:
#                     print('1. link_end =', link_end)
#                     time.sleep(2.6)
#                     try:
#                         iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                         if iframe2_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                        
#                     time.sleep(2.9)
#                     driver.get(link_end)
#                     context_book_scrap["link_end"] = "yes link_end"
                    
#         except NoSuchElementException:
#             print("NoSuchElementException iframe2")                       

#             time.sleep(4.3)
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
                    
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"

#             except NoSuchElementException:
#                 print("1. NoSuchElementException link_end")
#                 context_book_scrap["link_end"] = "no link_end"
#                 time.sleep(1.6)
#                 # driver.close()
#                 # time.sleep(1.2)
#                 # driver.quit()
#                 # time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 print("5. END book_scrap")
#                 return result_bot             
                            
#         time.sleep(14.2)
#         if context_book_scrap["link_end"] == "yes link_end":        
#             try:
#                 driver.execute_script("window.open()")
#                 # driver.execute_script("window.open()")
#                 # driver.switch_to.window(driver.window_handles[1])
#                 time.sleep(1.2)
#                 driver.switch_to.window(driver.window_handles[1])
#                 driver.get("chrome://downloads/")
#                 time.sleep(3.4)
#                 try:
#                     downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                     if downloaded_book:
#                         try:
#                             download_book_get_attribute = downloaded_book.get_attribute("href")
#                             # context_book_scrap["link_first"]
#                             if context_book_scrap["link_first"] == "link first confirmed":
#                                 context_book_scrap["pdf_link"] = "link pdf confirmed"
#                                 book_scrap.pdf_url_download_found = download_book_get_attribute
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()  
#                             else:
#                                 book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                                 context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()         
#                         except Exception as e:
#                             print(f"serializer.save url_pdf Exception as {e}")
                        
#                         # try:
#                         #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                         #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                         #     driver.execute_script("arguments[0].click()", show_book_my)
#                         # except JavascriptException:
#                         #     print("JavascriptException show_book_my") 
                            
#                         file_name_found = downloaded_book.text
#                         print("file_name_found =", file_name_found)
#                         # if file_name_found[:len(file_name)] == file_name:
#                         if pdf_search_filename in file_name_found:
#                             pdf_url_download = book_scrap.pdf_url_download_found
                            
#                             print(f'1. pdf_url_download = {pdf_url_download}')
#                             print("SUCCESS !!! " * 5)
#                             # driver.execute_script("arguments[0].click()", downloaded_book)
#                             time.sleep(4.6)
                            
#                             try:
#                                 show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                                 if show_book:
#                                     print("2a.show_book.text =", show_book.text)
#                                     try:
#                                         show_title_path = show_book.get_attribute("title")
#                                         if show_title_path:
#                                             print("2a. show_title_path =", show_title_path)
#                                             context_book_scrap["show_title_path"] = show_title_path
#                                     except NoSuchAttributeException:
#                                         print("2a. NoSuchAttributeException show_title_path")
                                        
#                                     try:
#                                         driver.execute_script("arguments[0].click()", show_book)
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                     except JavascriptException:
#                                         print("1. JavascriptException show_book")
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             # driver.quit()


#                             except NoSuchElementException:
#                                 print(f"NoSuchElementException show_book") 
#                                 time.sleep(2.6)
#                                 try:
#                                     driver.close()
#                                     driver.switch_to.window(driver.window_handles[0])
#                                     # time.sleep(1.2)
#                                     # driver.close()
#                                     # time.sleep(2.2)
#                                     # driver.quit()                            
#                                 except NoSuchDriverException:
#                                     print("1. NoSuchDriverException switch_to")

#                 except JavascriptException:
#                     print("2a. JavascriptException")
                    
#                     try:
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.pdf_url_download_found = "link pdf exist"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()    
#                     except Exception as e:
#                         print(f"2. link pdf exist Exception as {e}")
#                     try:
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()                            
#                     except NoSuchDriverException:
#                         print("1. NoSuchDriverException switch_to")
#                         time.sleep(2.2)
#                         # driver.quit()                                
                            
#                         # time.sleep(1.6)
#                         # driver.close()
#                         # time.sleep(1.2)
#                         # driver.quit()
#                         # time.sleep(2.3)
#                         # try:
#                         #     driver = book_scrap.run_driver
#                         #     kill_chrome(get_pid(driver))
#                         # except Exception as e:
#                         #     print(f"332 kill_chrome Exception as {e}")
                        
                                                
#             except Exception as e:
#                 print(f"window.open() Exception as {e}")
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(6.4)
#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver..window_handles[0]")

#             try:
#                 print('2a. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#                 file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#                 if file_exist:
#                     print("2a. file_exist")
#                     print("2a. SUCCESS !!! " * 10)
#                     try:
#                         print("2a. result_bot")
#                         time.sleep(2.6)
#                         # driver.close()
#                         # driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()
#                         print("2a_4. END book_scrap")
#                         return result_bot 
#                     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                         print(f"2a. RequestException, NewConnectionError = {err}")
#                         print("2a_4e. END book_scrap")
#                         return result_bot

#                 else:
#                     print("2a. no book in folder")
#                     context_book_scrap["book_in_folder"] = "no book in folder"
#                     time.sleep(4.3)                

#             except Exception as e:
#                 print(f"3. except file_exist: Exception as {e}")
                                       
#             # try:
#             #     home = os.path.expanduser("~")
#             #     downloadspath=os.path.join(home, "Downloads")
#             #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#             #     latest_file = max(list_of_files, key=os.path.getctime)
#             #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#             #     name_last_file = latest_file.split("\\")[-1][:-4]
#             #     if name_last_file[:len(pdf_search_filename)+1] == pdf_search_filename:
#             #         print("SUCCESS !!! " * 10)
#             #         try:
#             #             print("2. last driver quit")
#             #             time.sleep(2.6)
#             #             driver.close()
#             #             driver.switch_to.window(driver.window_handles[0])
#             #             time.sleep(1.2)
#             #             driver.close()
#             #             time.sleep(2.2)
#             #             driver.quit()
#             #             print("6. END book_scrap")
#             #             return result_bot 
                    
#             #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#             #             print(f"2. RequestException, NewConnectionError = {err}")                    

#             #     else:
#             #         print("2. no book in folder")
#             #         context_book_scrap["book_in_folder"] = "no book in folder"
                    
#             # except Exception as e:
#             #     print(f"1402 except file exist: Exception as {e}")
                    
#         elif context_book_scrap["link_end"] == "yes link_end":            
                        
#             try:
#                 dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                 try:
#                     action.move_to_element(dissmiss_button)
#                     time.sleep(0.3)
#                     action.click(dissmiss_button)
#                     action.perform()
#                 except MoveTargetOutOfBoundsException:
#                     print("MoveTargetOutOfBoundsException dissmiss-button")
                
#             except NoSuchElementException:
#                 print(f"NoSuchElementException dissmiss_button")  
#                 time.sleep(2.1)
#                 try:
#                     dissmiss_button = driver.find_element(By.ID, "dissmiss-button")
#                     try:
#                         action.move_to_element(dissmiss_button)
#                         time.sleep(0.3)
#                         action.click(dissmiss_button)
#                         action.perform()
#                     except MoveTargetOutOfBoundsException:
#                         print("MoveTargetOutOfBoundsException dissmiss-button")
                    
#                 except NoSuchElementException:
#                     print(f"NoSuchElementException dissmiss_button") 
                                        
#             time.sleep(2.6)              
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"
#             except NoSuchElementException:
#                 print("NoSuchElementException iframe2")                       

#                 time.sleep(4.3)
#                 try:
#                     element_link_end = driver.find_element(By.ID, "iframe2")
#                     if element_link_end:
#                         element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                         print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                         link_end = element_link_end.get_attribute('data-pdf-url')
                        
#                         if link_end != None:
#                             print('1. link_end =', link_end)
#                             time.sleep(2.6)
#                             try:
#                                 iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                                 if iframe2_header:
#                                     try:
#                                         driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                     except JavascriptException:
#                                         print("1. JavascriptException scrollBy")
#                             except NoSuchElementException:
#                                 print("NoSuchElementException watch_header")
                                
#                             time.sleep(2.9)
#                             driver.get(link_end)
#                             context_book_scrap["link_end"] = "yes link_end"

#                 except NoSuchElementException:
#                     print("1. NoSuchElementException link_end")            
                
#                     try:
#                         time.sleep(2.6)
#                         driver.close()
#                         time.sleep(2.2)
#                         driver.quit()
#                         time.sleep(2.2)
#                         print("7. END book_scrap")
#                         return result_bot 
                    
#                     except NoSuchDriverException:
#                         print("NoSuchDriverException driver.quit")  
                        
#     if context_book_scrap["link_end"] == "yes link_end":                    
#         try:
#             driver.execute_script("window.open()")
#             # driver.execute_script("window.open()")
#             # driver.switch_to.window(driver.window_handles[1])
#             time.sleep(1.2)
#             driver.switch_to.window(driver.window_handles[1])
#             driver.get("chrome://downloads/")
#             time.sleep(3.4)
#             try:
#                 downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                 if downloaded_book:
#                     try:
#                         download_book_get_attribute = downloaded_book.get_attribute("href")
#                         # context_book_scrap["link_first"]
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             context_book_scrap["pdf_link"] = "link pdf confirmed"
#                             book_scrap.pdf_url_download_found = download_book_get_attribute
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()  
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                             print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()         
#                     except Exception as e:
#                         print(f"serializer.save url_pdf Exception as {e}")
                    
#                     # try:
#                     #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                     #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                     #     driver.execute_script("arguments[0].click()", show_book_my)
#                     # except JavascriptException:
#                     #     print("JavascriptException show_book_my") 
                        
#                     file_name_found = downloaded_book.text
#                     print("file_name_found =", file_name_found)
#                     # if file_name_found[:len(file_name)] == file_name:
#                     if pdf_search_filename in file_name_found:
#                         pdf_url_download = book_scrap.pdf_url_download_found
                        
#                         print(f'1. pdf_url_download = {pdf_url_download}')
#                         print("SUCCESS !!! " * 5)
#                         # driver.execute_script("arguments[0].click()", downloaded_book)
#                         time.sleep(4.6)
                        
#                         try:
#                             show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                             if show_book:
#                                 print("3a. show_book.text =", show_book.text)
#                                 try:
#                                     show_title_path = show_book.get_attribute("title")
#                                     if show_title_path:
#                                         print("3a. show_title_path =", show_title_path)
#                                         context_book_scrap["show_title_path"] = show_title_path
#                                 except NoSuchAttributeException:
#                                     print("3a. NoSuchAttributeException show_title_path")
#                                 try:
#                                     driver.execute_script("arguments[0].click()", show_book)
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         time.sleep(1.2)
#                                         driver.close()
#                                         time.sleep(2.2)
#                                         driver.quit()
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
#                                         # driver.quit()
#                                 except JavascriptException:
#                                     print("1. JavascriptException show_book")
#                                     time.sleep(2.6)
#                                     try:
#                                         driver.close()
#                                         driver.switch_to.window(driver.window_handles[0])
#                                         # time.sleep(1.2)
#                                         # driver.close()
#                                         # time.sleep(2.2)
#                                         # driver.quit()
#                                     except NoSuchDriverException:
#                                         print("1. NoSuchDriverException switch_to")
#                                         time.sleep(2.2)
#                                         # driver.quit()


#                         except NoSuchElementException:
#                             print(f"NoSuchElementException show_book") 
#                             time.sleep(2.6)
#                             try:
#                                 driver.close()
#                                 driver.switch_to.window(driver.window_handles[0])
#                                 time.sleep(1.2)
#                                 # driver.close()
#                                 # time.sleep(2.2)
#                                 # driver.quit()                            
#                             except NoSuchDriverException:
#                                 print("1. NoSuchDriverException switch_to")
#                                 # time.sleep(2.2)
#                                 # driver.quit()


#             # except NoSuchShadowRootException:
#             #     print("1. NoSuchShadowRootException downloaded_book")
#             except JavascriptException:
#                 print("3a. JavascriptException")
                
#                 try:
#                     if context_book_scrap["link_first"] == "link first confirmed":
#                         book_scrap.pdf_url_download_found = "link pdf exist"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()
#                     else:
#                         book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                         pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                         serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                         if serializer.is_valid():
#                             serializer.save()    
#                 except Exception as e:
#                     print(f"2. link pdf exist Exception as {e}")
#                 try:
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()                            
#                 except NoSuchDriverException:
#                     print("1. NoSuchDriverException switch_to")
#                     time.sleep(2.2)
#                     # driver.quit()                                
                        
#                     # time.sleep(1.6)
#                     # driver.close()
#                     # time.sleep(1.2)
#                     # driver.quit()
#                     # time.sleep(2.3)
#                     # try:
#                     #     driver = book_scrap.run_driver
#                     #     kill_chrome(get_pid(driver))
#                     # except Exception as e:
#                     #     print(f"332 kill_chrome Exception as {e}")
                    
                                            
#         except Exception as e:
#             print(f"window.open() Exception as {e}")
#             try:
#                 time.sleep(2.6)
#                 driver.close()
#                 driver.switch_to.window(driver.window_handles[0])
#                 time.sleep(6.4)
#             except NoSuchDriverException:
#                 print("NoSuchDriverException driver..window_handles[0]")            
#             # try:
#             #     driver = book_scrap.run_driver
#             #     kill_chrome(get_pid(driver))
#             # except Exception as e:
#             #     print(f"332 kill_chrome Exception as {e}")            

#         try:
#             print('3a. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#             file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#             if file_exist:
#                 print("3a. file_exist")
#                 print("3a. SUCCESS !!! " * 10)
#                 try:
#                     print("3a. result_bot")
#                     time.sleep(2.6)
#                     # driver.close()
#                     # driver.switch_to.window(driver.window_handles[0])
#                     # time.sleep(1.2)
#                     # driver.close()
#                     # time.sleep(2.2)
#                     # driver.quit()
#                     # print("3a_4. END book_scrap")
#                     return result_bot 
#                 except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                     print(f"3a. RequestException, NewConnectionError = {err}")
#                     print("3a_4e. END book_scrap")
#                     return result_bot

#             else:
#                 print("3a. no book in folder")
#                 context_book_scrap["book_in_folder"] = "no book in folder"
#                 time.sleep(4.3)  
#         except Exception as e:
#             print(f"3a. except file_exist: Exception as {e}") 
                                                        
#         # try:
#         #     home = os.path.expanduser("~")
#         #     downloadspath=os.path.join(home, "Downloads")
#         #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#         #     latest_file = max(list_of_files, key=os.path.getctime)
#         #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#         #     name_last_file = latest_file.split("\\")[-1][:-4]
#         #     if name_last_file[:len(pdf_search_filename)+1] == pdf_search_filename:
#         #         print("SUCCESS !!! " * 10)
                
#         #         try:
#         #             print("3. book in folder")
#         #             context_book_scrap["book_in_folder"] = "book in folder"
#         #             time.sleep(2.6)
#         #             driver.close()
#         #             driver.switch_to.window(driver.window_handles[0])
#         #             time.sleep(1.2)
#         #             driver.close()
#         #             time.sleep(2.2)
#         #             driver.quit()
#         #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         #             print(f"3. RequestException, NewConnectionError = {err}")
#         #     else:
#         #         print("3. no book in folder")
#         #         context_book_scrap["book_in_folder"] = "no book in folder"
#         #         time.sleep(4.3)
                
#         # except Exception as e:
#         #     print(f"except file exist: Exception as {e}") 

    
#     elif context_book_scrap["link_end"] != "yes link_end" or context_book_scrap["book_in_folder"] != "book in folder": 
                
#         try:
#             element_link_end = driver.find_element(By.ID, "iframe2")
#             if element_link_end:
#                 element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                 print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                 link_end = element_link_end.get_attribute('data-pdf-url')
#                 if link_end != None:
#                     print('1. link_end =', link_end)
#                     time.sleep(2.6)
#                     try:
#                         iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                         if iframe2_header:
#                             try:
#                                 driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                             except JavascriptException:
#                                 print("1. JavascriptException scrollBy")
#                     except NoSuchElementException:
#                         print("NoSuchElementException watch_header")
                        
#                     time.sleep(2.9)
#                     driver.get(link_end)
#                     context_book_scrap["link_end"] = "yes link_end"
                    
#         except NoSuchElementException:
#             print("NoSuchElementException iframe2")                       

#             time.sleep(4.3)
#             try:
#                 element_link_end = driver.find_element(By.ID, "iframe2")
#                 if element_link_end:
#                     element_link_end_outer = element_link_end.get_attribute("outerHTML")
#                     print("2. element_link_end_outer =", element_link_end_outer[0:element_link_end_outer.find(">") + 1])
#                     link_end = element_link_end.get_attribute('data-pdf-url')
                    
#                     if link_end != None:
#                         print('1. link_end =', link_end)
#                         time.sleep(2.6)
#                         try:
#                             iframe2_header = driver.find_element(By.CLASS_NAME, "pdf-pro-meta-border")
#                             if iframe2_header:
#                                 try:
#                                     driver.execute_script("return arguments[0].scrollIntoView(true);", iframe2_header)
#                                 except JavascriptException:
#                                     print("1. JavascriptException scrollBy")
#                         except NoSuchElementException:
#                             print("NoSuchElementException watch_header")
                            
#                         time.sleep(2.9)
#                         driver.get(link_end)
#                         context_book_scrap["link_end"] = "yes link_end"

#             except NoSuchElementException:
#                 print("1. NoSuchElementException link_end")
#                 context_book_scrap["link_end"] = "no link_end"
#                 time.sleep(1.6)
#                 driver.close()
#                 time.sleep(1.2)
#                 driver.quit()
#                 time.sleep(2.3)
#                 # try:
#                 #     driver = book_scrap.run_driver
#                 #     kill_chrome(get_pid(driver))
#                 # except Exception as e:
#                 #     print(f"332 kill_chrome Exception as {e}")
                    
#                 print("5. END book_scrap")
#                 return result_bot             
                            
#         time.sleep(14.2)
#         if context_book_scrap["link_end"] == "yes link_end":        
#             try:
#                 driver.execute_script("window.open()")
#                 # driver.execute_script("window.open()")
#                 # driver.switch_to.window(driver.window_handles[1])
#                 time.sleep(1.2)
#                 driver.switch_to.window(driver.window_handles[1])
#                 driver.get("chrome://downloads/")
#                 time.sleep(3.4)
#                 try:
#                     downloaded_book =  driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#file-link")')
#                     if downloaded_book:
#                         try:
#                             download_book_get_attribute = downloaded_book.get_attribute("href")
#                             # context_book_scrap["link_first"]
#                             if context_book_scrap["link_first"] == "link first confirmed":
#                                 context_book_scrap["pdf_link"] = "link pdf confirmed"
#                                 book_scrap.pdf_url_download_found = download_book_get_attribute
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()  
#                             else:
#                                 book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                                 context_book_scrap["pdf_link"] = "link pdf unconfirmed"                            
#                                 print("book_scrap.pdf_url_download_found =", book_scrap.pdf_url_download_found)
#                                 pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                                 serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                                 if serializer.is_valid():
#                                     serializer.save()         
#                         except Exception as e:
#                             print(f"serializer.save url_pdf Exception as {e}")
                        
#                         # try:
#                         #     # show_book_my = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                         #     show_book_my = driver.execute_script("return arguments[0].parentElement.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.firstElementChild.firstElementChild", downloaded_book)
#                         #     driver.execute_script("arguments[0].click()", show_book_my)
#                         # except JavascriptException:
#                         #     print("JavascriptException show_book_my") 
                            
#                         file_name_found = downloaded_book.text
#                         print("file_name_found =", file_name_found)
#                         # if file_name_found[:len(file_name)] == file_name:
#                         if pdf_search_filename in file_name_found:
#                             pdf_url_download = book_scrap.pdf_url_download_found
                            
#                             print(f'1. pdf_url_download = {pdf_url_download}')
#                             print("SUCCESS !!! " * 5)
#                             # driver.execute_script("arguments[0].click()", downloaded_book)
#                             time.sleep(4.6)
                            
#                             try:
#                                 show_book = driver.execute_script('return document.querySelector("body > downloads-manager").shadowRoot.querySelector("#frb0").shadowRoot.querySelector("#show")')
#                                 if show_book:
#                                     print("4a. show_book.text =", show_book.text)
#                                     try:
#                                         show_title_path = show_book.get_attribute("title")
#                                         if show_title_path:
#                                             print("4a. show_title_path =", show_title_path)
#                                             context_book_scrap["show_title_path"] = show_title_path
#                                     except NoSuchAttributeException:
#                                         print("4a. NoSuchAttributeException show_title_path")
#                                     try:
#                                         driver.execute_script("arguments[0].click()", show_book)
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                     except JavascriptException:
#                                         print("1. JavascriptException show_book")
#                                         time.sleep(2.6)
#                                         try:
#                                             driver.close()
#                                             driver.switch_to.window(driver.window_handles[0])
#                                             time.sleep(1.2)
#                                             driver.close()
#                                             time.sleep(2.2)
#                                             driver.quit()
#                                         except NoSuchDriverException:
#                                             print("1. NoSuchDriverException switch_to")
#                                             time.sleep(2.2)
#                                             driver.quit()


#                             except NoSuchElementException:
#                                 print(f"NoSuchElementException show_book") 
#                                 time.sleep(2.6)
#                                 try:
#                                     driver.close()
#                                     driver.switch_to.window(driver.window_handles[0])
#                                     # time.sleep(1.2)
#                                     # driver.close()
#                                     # time.sleep(2.2)
#                                     # driver.quit()                            
#                                 except NoSuchDriverException:
#                                     print("1. NoSuchDriverException switch_to")

#                 except JavascriptException:
#                     print("2a. JavascriptException")
                    
#                     try:
#                         if context_book_scrap["link_first"] == "link first confirmed":
#                             book_scrap.pdf_url_download_found = "link pdf exist"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()
#                         else:
#                             book_scrap.pdf_url_download_found = "link pdf unconfirmed"
#                             pdf_url_download_found_serializer = book_scrap.pdf_url_download_found
#                             serializer = BookPdfUrlSerializer(book_pdf_bot, data={'url_pdf': pdf_url_download_found_serializer}, partial=True)
#                             if serializer.is_valid():
#                                 serializer.save()    
#                     except Exception as e:
#                         print(f"2. link pdf exist Exception as {e}")
#                     try:
#                         driver.close()
#                         driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()                            
#                     except NoSuchDriverException:
#                         print("1. NoSuchDriverException switch_to")
#                         time.sleep(2.2)
#                         # driver.quit()                                
                            
#                         # time.sleep(1.6)
#                         # driver.close()
#                         # time.sleep(1.2)
#                         # driver.quit()
#                         # time.sleep(2.3)
#                         # try:
#                         #     driver = book_scrap.run_driver
#                         #     kill_chrome(get_pid(driver))
#                         # except Exception as e:
#                         #     print(f"332 kill_chrome Exception as {e}")
                        
                                                
#             except Exception as e:
#                 print(f"window.open() Exception as {e}")
#                 try:
#                     time.sleep(2.6)
#                     driver.close()
#                     driver.switch_to.window(driver.window_handles[0])
#                     time.sleep(6.4)
#                 except NoSuchDriverException:
#                     print("NoSuchDriverException driver..window_handles[0]")

#             try:
#                 print('4a. context_book_scrap["show_title_path"] =', context_book_scrap["show_title_path"])
#                 file_exist = os.path.isfile(context_book_scrap["show_title_path"])
#                 if file_exist:
#                     print("4a. file_exist")
#                     print("4a. SUCCESS !!! " * 10)
#                     try:
#                         print("4a. result_bot")
#                         time.sleep(2.6)
#                         # driver.close()
#                         # driver.switch_to.window(driver.window_handles[0])
#                         # time.sleep(1.2)
#                         # driver.close()
#                         # time.sleep(2.2)
#                         # driver.quit()
#                         # print("4a_4. END book_scrap")
#                         return result_bot 
#                     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#                         print(f"4a. RequestException, NewConnectionError = {err}")
#                         print("4a_4e. END book_scrap")
#                         return result_bot

#                 else:
#                     print("4a. no book in folder")
#                     context_book_scrap["book_in_folder"] = "no book in folder"
#                     time.sleep(4.3)  
#             except Exception as e:
#                 print(f"4a. except file_exist: Exception as {e}") 
                                  
#             # try:
#             #     home = os.path.expanduser("~")
#             #     downloadspath=os.path.join(home, "Downloads")
#             #     list_of_files = glob.glob(downloadspath+"\*.pdf") # * means all if need specific format then *.csv
#             #     latest_file = max(list_of_files, key=os.path.getctime)
#             #     print(latest_file) # C:\Users\BONUM\Downloads\Dickens Karol - Wielkie nadzieje.pdf
#             #     name_last_file = latest_file.split("\\")[-1][:-4]
#             #     if name_last_file[:len(pdf_search_filename)+1] == pdf_search_filename:
#             #         print("SUCCESS !!! " * 10)
#             #         try:
#             #             print("2. last driver quit")
#             #             time.sleep(2.6)
#             #             driver.close()
#             #             driver.switch_to.window(driver.window_handles[0])
#             #             time.sleep(1.2)
#             #             driver.close()
#             #             time.sleep(2.2)
#             #             driver.quit()
#             #             print("6. END book_scrap")
#             #             return result_bot 
                    
#             #         except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#             #             print(f"2. RequestException, NewConnectionError = {err}")                    

#             #     else:
#             #         print("2. no book in folder")
#             #         context_book_scrap["book_in_folder"] = "no book in folder"
                    
#             # except Exception as e:
#             #     print(f"1402 except file exist: Exception as {e}")
        
         
#     try:
#         print("2050. last driver quit")
#         time.sleep(2.6)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#         time.sleep(1.2)
#         driver.close()
#         time.sleep(2.2)
#         driver.quit()
#     except (RequestException, NewConnectionError, ConnectionError,  MaxRetryError) as err:
#         print(f"RequestException, NewConnectionError = {err}")  

#     # try:
#     #     time.sleep(1.6)
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)
#     #     try:
#     #         driver = book_scrap.run_driver
#     #         kill_chrome(get_pid(driver))
#     #     except Exception as e:
#     #         print(f"332 kill_chrome Exception as {e}")
#     #         # os.system('cmd /k "taskkill /F /IM chrome.exe /T"')
#     # except NoSuchDriverException:
#     #     print("NoSuchDriverException")
#     # try:
#     #     driver.execute_script("window.close()")
#     # except JavascriptException:
#     #     print("avascriptException")
#     # time.sleep(1.6)
#     # try:
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)
#     # except NoSuchDriverException:
#     #     print("NoSuchDriverException driver.quit")
        
#     # try:
#     #     driver.get("https://www.bing.com/")
#     #     time.sleep(2.4)
#     #     driver.close()
#     #     time.sleep(1.2)
#     #     driver.quit()
#     #     time.sleep(2.3)     
#     # except Exception as e:
#     #     print(f"bing Exception as {e}")   
        
#     print("8. END book_scrap")  
      
#     return result_bot  