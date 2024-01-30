import requests, random, time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as Remote
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.alert import Alert
import os.path
import undetected_chromedriver as uc
import os
import re
import glob
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoSuchShadowRootException, ScreenshotException, JavascriptException, MoveTargetOutOfBoundsException, NoSuchDriverException, UnexpectedAlertPresentException
# from shiftlab_ocr.doc2text.reader import Reader
from PIL import Image
from django.conf import settings
from bookmain import settings as my_settings
from django.conf.urls.static import static
# def scrap(request):
import io
import urllib.request
# import easyocr
import signal
from pyshadow.main import Shadow
import subprocess
from fake_useragent import UserAgent

starttime = time.time()

def get_pid(driver):
    chromepid = int(driver.service.process.pid)
    print("chromepid =", chromepid)
    return (chromepid)

def kill_chrome(pid):
    try:
        print("pid =", pid)
        os.kill(pid, signal.SIGTERM)
        return 1
    except Exception as e:
        print(f"Exception as {e}")
        return 0
    
# https://gist.github.com/sujit/578d577c3f5a74a9f183c92a2c18c5b5    
# https://stackoverflow.com/questions/24507078/how-to-deal-with-certificates-using-selenium
def get_chrome_capabilities(capabilities, chrome_options):
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # capabilities = DesiredCapabilities.CHROME.copy()
        
    capabilities['acceptSslCerts'] = True
    capabilities['acceptInsecureCerts'] = True
    capabilities["pageLoadStrategy"] = "none"
    # opts = webdriver.ChromeOptions()
    capabilities.update(chrome_options.to_capabilities())
    # chrome_options = uc.ChromeOptions()
    
    return capabilities

def body_content_visibility(shadow_driver, wait_9, wait_6):
    try:
        body_content = (By.CSS_SELECTOR, "body")
        element_body =  wait_9.until(EC.presence_of_element_located(body_content))
        if element_body:
            print("1. body_content_visibility() YES element_body")
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_body)
            except JavascriptException:
                print("1. body_content_visibility() JavascriptException visibility")    
                time.sleep(0.4)
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_body)
                except JavascriptException:
                    print("1. body_content_visibility() JavascriptException visibility")  
    except TimeoutException:
        print("1. body_content_visibility() TimeoutException visibility")   
        time.sleep(1.6)
        try:
            body_content = (By.CSS_SELECTOR, "body")
            element_body = wait_6.until(EC.presence_of_element_located(body_content))
            if element_body:
                print("2. body_content_visibility() YES element_body")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_body)
                except JavascriptException:
                    print("2. body_content_visibility() JavascriptException visibility")    
                    time.sleep(0.4)
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_body)
                    except JavascriptException:
                        print("2. body_content_visibility() JavascriptException visibility")  
        except TimeoutException:
            print("2. body_content_visibility() TimeoutException element_body") 

def html_content_visibility(shadow_driver, wait_9, wait_6):
    try:
        html_content = (By.CSS_SELECTOR, "html")
        element_html =  wait_9.until(EC.presence_of_element_located(html_content))
        # if element_html:
        try:
            shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_html)
            print("1. try html_content_visibility() YES element_html")
        except JavascriptException:
            print("1. html_content_visibility() JavascriptException visibility")    
            time.sleep(0.4)
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_html)
            except JavascriptException:
                print("1. html_content_visibility() JavascriptException visibility")  
    except TimeoutException:
        print("1. html_content_visibility() TimeoutException visibility")   
        time.sleep(1.6)
        try:
            html_content = (By.CSS_SELECTOR, "html")
            element_html = wait_6.until(EC.presence_of_element_located(html_content))
            if element_html:
                print("2. html_content_visibility() YES element_html")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_html)
                except JavascriptException:
                    print("2. html_content_visibility() JavascriptException visibility")    
                    time.sleep(0.4)
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden';", element_html)
                    except JavascriptException:
                        print("2. html_content_visibility() JavascriptException visibility")  
        except TimeoutException:
            print("2. html_content_visibility() TimeoutException element_html") 
            
            
def html_content_opacity_0(shadow_driver, wait_9, wait_6):
    try:
        html_content = (By.CSS_SELECTOR, "html")
        element_html =  wait_9.until(EC.presence_of_element_located(html_content))
        if element_html:
            print("1. html_content_opacity_0() YES element_html")
            try:
                shadow_driver.execute_script("arguments[0].style.opacity = '0';", element_html)
            except JavascriptException:
                print("1. html_content_opacity_0() JavascriptException opacity")    
                time.sleep(0.4)
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'visible';", element_html)
                time.sleep(0.4)              
            except JavascriptException:
                print("1. html_content_opacity_0() JavascriptException visibility")  
    except TimeoutException:
        print("1. html_content_opacity_0() TimeoutException element_html")   
        time.sleep(1.6)
        try:
            html_content = (By.CSS_SELECTOR, "html")
            element_html = wait_6.until(EC.presence_of_element_located(html_content))
            if element_html:
                print("2. html_content_opacity_0() YES element_html")
                try:
                    shadow_driver.execute_script("arguments[0].style.opacity = '0';", element_html)
                except JavascriptException:
                    print("2. html_content_opacity_0() JavascriptException opacity")    
                    time.sleep(0.4)
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'visible';", element_html)
                except JavascriptException:
                    print("2. html_content_opacity_0() JavascriptException visibility") 
                    time.sleep(0.4)
        except TimeoutException:
            print("2. html_content_opacity_0() TimeoutException element_html")  
            
def html_content_opacity_1(shadow_driver, wait_9, wait_6):
    try:
        html_content = (By.CSS_SELECTOR, "html")
        element_html =  wait_9.until(EC.presence_of_element_located(html_content))
        if element_html:
            print("1. html_content_opacity_1() YES element_html")
            try:
                shadow_driver.execute_script("arguments[0].style.opacity = '1';", element_html)
            except JavascriptException:
                print("1. html_content_opacity_1() JavascriptException opacity")    
                time.sleep(0.4)
                try:
                    shadow_driver.execute_script("arguments[0].style.opacity = '1';", element_html)
                except JavascriptException:
                    print("1. JavascriptException opacity")  
    except TimeoutException:
        print("1. html_content_opacity_1() TimeoutException element_html")   
        time.sleep(1.6)
        try:
            html_content = (By.CSS_SELECTOR, "html")
            element_html = wait_6.until(EC.presence_of_element_located(html_content))
            if element_html:
                print("v YES element_html")
                try:
                    shadow_driver.execute_script("arguments[0].style.opacity = '1';", element_html)
                except JavascriptException:
                    print("1. html_content_opacity_1() JavascriptException opacity")    
                    time.sleep(0.4)
                    try:
                        shadow_driver.execute_script("arguments[0].style.opacity = '1';", element_html)
                    except JavascriptException:
                        print("1. html_content_opacity_1() JavascriptException opacity")  
        except TimeoutException:
            print("1. html_content_opacity_1() TimeoutException element_html")                       


def bars_hidden(shadow_driver, action):
    # time.sleep(1.8)

    try:
        info_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > info-icon")')
        
        if info_bar:
            print("bars_hidden() YES info_bar") 
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", info_bar)
            except JavascriptException:
                print("bars_hidden() JavascriptException info_bar")
                
                time.sleep(2.6)
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", info_bar)
                except JavascriptException:
                    print("bars_hidden() JavascriptException info_bar")                         

    except JavascriptException as err:
        print("bars_hidden() JavascriptException, NoSuchShadowRootException info_bar except: { err }")     
        time.sleep(6.3)
        try:
            info_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > info-icon")')
            if info_bar:
                print("bars_hidden() YES info_bar") 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", info_bar)
                except JavascriptException:
                    print("bars_hidden() JavascriptException info_bar") 
                    time.sleep(2.6)
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", info_bar)
                    except JavascriptException:
                        print("bars_hidden() JavascriptException info_bar")                            

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("bars_hidden() JavascriptException, NoSuchShadowRootException info_bar except: { err }")
             
    time.sleep(4.1)          
    try:
        actiongroup = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div.actiongroup")')
        if actiongroup:
            print("bars_hidden() YES actiongroup")
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                
            except JavascriptException:
                print("bars_hidden() JavascriptException")  
                time.sleep(3.2) 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                    
                except JavascriptException:
                    print("bars_hidden() JavascriptException")  
                    time.sleep(3.2)                     
        
    except JavascriptException:
        print("bars_hidden() NO actiongroup")  

        time.sleep(4.5)
        try:
            actiongroup = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div.actiongroup")')
            if actiongroup:
                print("bars_hidden() YES actiongroup")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                    
                except JavascriptException:
                    print("bars_hidden() JavascriptException")  
                    time.sleep(3.2) 
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                        
                    except JavascriptException:
                        print("bars_hidden() JavascriptException")  
                        time.sleep(3.2)                     
            
        except JavascriptException:
            print("bars_hidden(). NO actiongroup")   
            
    # time.sleep(1.4)    
    # shadow_driver.maximize_window()
    # time.sleep(0.3)
    # shadow_driver.fullscreen_window()
    time.sleep(1.4)      
    try:
        left_buttons = shadow_driver.execute_script('return document.querySelector("#theatre-ia > div.row > div > ia-book-theater").shadowRoot.querySelector("ia-bookreader").shadowRoot.querySelector("div > iaux-item-navigator").shadowRoot.querySelector("#frame > div > nav > div.minimized")')
        if left_buttons:
            print("bars_hidden() YES left_buttons")
            try: 
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                print("bars_hidden() yes hidden left_buttons")
            except JavascriptException:
                print("bars_hidden() no hidden left_buttons")
                try: 
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                    print("bars_hidden() yes hidden left_buttons")
                except JavascriptException:
                    print("bars_hidden() no hidden left_buttons")                
                                
    # except NoSuchElementException:
    except (JavascriptException, NoSuchShadowRootException) as err:
        print("bars_hidden() JavascriptException, NoSuchShadowRootException left_buttons except: { err }") 
        print("bars_hidden() NO left_buttons") 
        time.sleep(3.1)                
        try:
            left_buttons = shadow_driver.execute_script('return document.querySelector("#theatre-ia > div.row > div > ia-book-theater").shadowRoot.querySelector("ia-bookreader").shadowRoot.querySelector("div > iaux-item-navigator").shadowRoot.querySelector("#frame > div > nav > div.minimized")')
            if left_buttons:
                print("bars_hidden() YES left_buttons")

                try: 
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                    print("bars_hidden() yes hidden left_buttons")
                except JavascriptException:
                    print("bars_hidden() no hidden left_buttons")
                    try: 
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                        print("bars_hidden() yes hidden left_buttons")
                    except JavascriptException:
                        print("bars_hidden() no hidden left_buttons")                    
                                
    # except NoSuchElementException:
        except (JavascriptException, NoSuchShadowRootException) as err:
            print("bars_hidden() JavascriptException, NoSuchShadowRootException left_buttons except: { err }") 

    time.sleep(1.3)
    try:
        # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button")
        fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
        if fullscreen_button:
            print("bars_hidden() YES fullscreen_button") 
            try:     
                action.move_to_element(fullscreen_button)
                time.sleep(0.5)
                action.click(fullscreen_button)
                action.perform()  
            except MoveTargetOutOfBoundsException:
                print("bars_hidden() MoveTargetOutOfBoundsException borrow_button")
                time.sleep(2.3)        
                try:     
                    shadow_driver.execute_script("arguments[0].click();", fullscreen_button)
                except JavascriptException:
                    print("bars_hidden() JavascriptException borrow_button")
                    time.sleep(2.3)   
                    
    except NoSuchElementException:
        print("1. bars_hidden() NO fullscreen_button")   
        time.sleep(2.9) 
        
        try:
            # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button") 
            # fullscreen_button = shadow_driver.execute_script('return document.querySelector("#BookReader > div.BRfooter > div > nav > ul > li:nth-child(10) > button")') 
            fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
            if fullscreen_button:
                print("1148. YES fullscreen_button")  
                        
                try:     
                    action.move_to_element(fullscreen_button)
                    time.sleep(0.5)
                    action.click(fullscreen_button)
                    action.perform()  
                    time.sleep(2.1)  
                    # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
                    # shadow_driver.get(current_book_url)
                except MoveTargetOutOfBoundsException:
                    print("1159a. MoveTargetOutOfBoundsException fullscreen_button")
                    time.sleep(2.3)        
                    try:     
                        shadow_driver.execute_script("arguments[0].click();", fullscreen_button)
                        time.sleep(2.1)  
                        # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
                        # shadow_driver.get(current_book_url)
                    except JavascriptException:
                        print("1167. JavascriptException fullscreen_button")
                        time.sleep(2.3)  
                        
        except NoSuchElementException:
            print("2. bars_hidden() NO fullscreen_button")   
            time.sleep(3.9)  
            # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
            # shadow_driver.get(current_book_url)
            # time.sleep(7.9) 
                
    time.sleep(2.7)        
    try:
        # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button")
        fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
        if fullscreen_button:
            print("bars_hidden() YES fullscreen_button") 
                   
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                print("397 yes hidden lfullscreen_button")
            except JavascriptException:
                print("bars_hidden() JavascriptException fullscreen_button hidden")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                    print("bars_hidden() yes hidden lfullscreen_button")
                except JavascriptException:
                    print("bars_hidden() JavascriptException fullscreen_button hidden")
                    
    except NoSuchElementException:
        print("3. bars_hidden() NO fullscreen_button")   
        time.sleep(2.9) 
        
        try:
            # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button") 
            # fullscreen_button = shadow_driver.execute_script('return document.querySelector("#BookReader > div.BRfooter > div > nav > ul > li:nth-child(10) > button")') 
            fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
            if fullscreen_button:
                print("bars_hidden() YES fullscreen_button")  
                        
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                    print("419. yes hidden lfullscreen_button")
                except JavascriptException:
                    print("bars_hidden() JavascriptException fullscreen_button hidden")
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                        print("bars_hidden() yes hidden lfullscreen_button")
                    except JavascriptException:
                        print("bars_hidden() JavascriptException fullscreen_button hidden")
                        
        except NoSuchElementException:
            print("4. bars_hidden() NO fullscreen_button")   
            time.sleep(3.9)  
            # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
            # shadow_driver.get(current_book_url)
            # time.sleep(7.9)             
    time.sleep(3.7)                     
    try:
        shadow_driver.execute_script("""
                document.addEventListener('keydown', (event) => {
                var name_1 = event.key;
                var name_2 = event.key;
                var name_3 = event.key;
                var code_1 = event.code;
                var code_2 = event.code;
                var code_3 = event.code;
                               
                if (name_1 === 'Control' && name_2 === 'Shift') {
                // Do nothing when only the Control key is pressed.
                event.preventDefault();
                alert("ctrl + shift");
                return;
                }
                
                if (event.ctrlKey && event.shiftKey && code_3 === "KeyI") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                } 
                
                if (event.ctrlKey && event.shiftKey && code_3 === "KeyU") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                } 
                
                if (event.ctrlKey && event.shiftKey && code_3 === "KeyC") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                } 
            
                if (event.ctrlKey && code_3 === "KeyU") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                }
                
                // if (event.key == "F12") {
                if (code_3 === "F12") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                } 
                
                if (event.key == "F11" || event.code == "F11") {
                    event.preventDefault();   
                    alert(` CHANGE SIZE NOT WORKING ;)`);
                }
                
                if (event.ctrlKey && event.key=="F5") {
                event.preventDefault();
                alert (" RELOAD SITE NOT WORKING ");
                }
                
                if (event.key == "Escape" || event.code == "Escape") {
                    event.preventDefault();
                    alert(` CHANGE SIZE NOT WORKING ;)`);          
                    document.body.blur();
                    event.preventDefault();
                    document.body.blur();
                    }     
                    
            }, false);        
                        
                                """)
    except (JavascriptException, UnexpectedAlertPresentException):
        print("1a. JavascriptException")
    try:
        close_text = shadow_driver.execute_script("""
        document.addEventListener('keydown', (event) => {
            var code_close = event.code;
            if (code_close === "Key0") {
                alert("close yes");
                txt = "yes";
                return txt
            }          
        }, false);  
        """)
        if close_text == "yes":
            time.sleep(1.2)
            shadow_driver.close()
            time.sleep(1.1)
            shadow_driver.quit()
    except JavascriptException:
        print("1b. JavascriptException")
                                                         

def read_archive(link_id, archive_title, context_read_archive):
    context_driver_read_archive = {}
    result_archive = "result_archive"
    context_driver_read_archive["unavailable_button"] = "unknown"
    context_driver_read_archive["return_button"] = "unknown"
    context_driver_read_archive["borrow_button"] = "unknown"
    shadow_driver_current_url = "unknown"
    result_archive = "result_archive"
    
    context_read_archive["read_archive_return_message"] = ""
    read_archive.return_message = ""
    context_read_archive["read_archive_link_pdf"] = ""
    read_archive.link_pdf = ""
    try:
        chrome_service = ChromeService
        chrome_options = uc.ChromeOptions()

        chrome_options.page_load_strategy = 'none'
        chrome_options.add_argument('--incognito')
        
        ua = UserAgent()
        # chrome_options.add_argument(f'user-agent={ua.random}')
        # print("user-agent={ ua.random } =", ua.random)
        
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--content-shell-hide-toolbar")
        chrome_options.add_argument("--top-controls-hide-threshold")
        #chrome_options.add_argument("--app-auto-launched")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--hide-scrollbars")
        # chrome_options.add_argument('--disable-gpu')
        
        # chrome_options.add_argument("--deny-permission-prompts")
        # chrome_options.add_argument("--disable-crash-reporter")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-in-process-stack-traces")
        # chrome_options.add_extention("CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_54_0_0.crx")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument("--disable-dev-shm-usage")   
        
        # chrome_options.add_argument('--allow-running-insecure-content')
        # chrome_options.add_argument('--unsafely-treat-insecure-origin-as-secure')
        chrome_options.add_argument('--force-show-cursor')
        chrome_options.add_argument("--mixed") 
            
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--no-zygote')
        chrome_options.add_argument('--disable-breakpad')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        # chrome_options.add_argument(f"--app=https://archive.org/*")
        chrome_options.add_argument("--excludeSwitches=['enable-automation']")
        # chrome_options.add_argument("--disable-popup-blocking") 
        
        chrome_options.add_argument("--start-maximized") 
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_argument("--kiosk")   
        
        chrome_options.add_experimental_option("prefs", {
            # "download.default_directory": r"C:\Users\xxx\downloads\Test",
            # "download.default_directory": "C:\Users\BONUM\Downloads\",
            # "download.default_directory": r"C:\Users\BONUM\Downloads",
            "download.prompt_for_download": False,
            # "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
            
            "useAutomationExtension": False,
            'excludeSwitches': ['enable-automation', 'enable-logging'],
            'androidPackage': 'com.android.chrome',
            # 'profile.managed_default_content_settings.javascript': 2,
            }) 
        
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")         
        chrome_options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        # path_extention = os.path.join(settings.STATIC_ROOT, "CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx")
        # chrome_options.add_extension(path_extention)
        
        # extension_file_path = os.path.abspath("booksmart-app\static\CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx")
        # extension_file_path = os.path.abspath("static/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx")
        # extension_file_path = static('CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx')
        # print("my_settings.STATIC_ROOT =", my_settings.STATIC_ROOT)
        # extension_file_path = f'{my_settings.STATIC_ROOT}\CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx'
        # try:
        #     # extension_file_path = "https://booksmart-app-bd32a8932ff0.herokuapp.com/static/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx"
        #     extension_file_path = f'{my_settings.STATIC_URL}CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx'
        #     print("extension_file_path =", extension_file_path)
        #     chrome_options.add_extension(extension_file_path)
        # except Exception as err:
        #     print(f"1. reader_archive extension_file_path Exception as {err}")
            # try:
                # extension_file_path = "https://booksmart-app-bd32a8932ff0.herokuapp.com/static/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0.crx"
            # except Exception as err:
                # print(f"2. reader_archive extension_file_path Exception as {err}")            
        
        # extension_folder_path = f'{my_settings.STATIC_ROOT}\CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_55_0_0'
        # chrome_options.add_argument(f'load-extension={extension_folder_path}')
        # driver = webdriver.Chrome(options=chrome_options, service=ChromeService(ChromeDriverManager().install()), )
        # capa = DesiredCapabilities.CHROME.copy()
        # capa["pageLoadStrategy"] = "none"
        # # capa['acceptSslCerts'] = True
        # capa['acceptInsecureCerts'] = True
        
        # driver = uc.Chrome(desired_capabilities=capa, options=chrome_options)  
        # driver = uc.Chrome(desired_capabilities=get_chrome_capabilities(), options=chrome_options) 
        capabilities = DesiredCapabilities.CHROME.copy()
        
        capabilities['acceptSslCerts'] = True
        capabilities['acceptInsecureCerts'] = True
        capabilities["pageLoadStrategy"] = "none"

        # capabilities.update(chrome_options.to_capabilities())
        # use_subprocess=False
        # service_args = []
        # service = ChromeService(service_args=['--disable-build-check'], log_output=subprocess.STDOUT)
        
        driver = uc.Chrome(service=ChromeService(ChromeDriverManager().install(), executable_path='./chromedriver.exe', service_args=['--disable-build-check'], log_output=subprocess.STDOUT), options=chrome_options, desired_capabilities=capabilities, )  
        # driver = uc.Chrome(options=chrome_options, desired_capabilities=capabilities, )    
        # get_chrome_capabilities():  
        driver.execute_script("Object.defineProperty(navigator, 'uc', {get: () => undefined})")
        shadow = Shadow(driver)
        context_driver_read_archive["shadow_headless"] = shadow
        shadow_driver = shadow.driver
        context_driver_read_archive["driver_headless"] = shadow_driver
        action = ActionChains(shadow_driver)
        context_driver_read_archive["driver_action_headless"] = action
        time.sleep(6.31)
        print("ALL options shadow_drive add")
        
        # shadow_driver.maximize_window()
        # shadow_driver.fullscreen_window()
        
    except Exception as err:
        print(f"1 reader_archive Exception as {err}")    
              
    time.sleep(1.3)
    try:
        # url_book = f"https://archive.org/details/{link_id}"
        url_book = f"https://archive.org/details/{link_id}/mode/2up"
        # https://archive.org/details/chrzestognia0000sapk/mode/2up?view=theater
        # shadow_driver = context_driver["driver_headless"]
        # action = context_driver["driver_action_headless"] 
        # shadow = context_driver["shadow_headless"] 
        time.sleep(0.2) 
        shadow_driver.get(url_book) 
    except Exception as err:
        print(f"2 reader_archive Exception as {err}")            
    
    # time.sleep(0.2)
    # try:
    #     shadow_driver.fullscreen_window()
    # except Exception as err:
    #     print(f"181. fullscreen_window() Exception as {err}") 
    #     time.sleep(0.6)
    #     try:
    #         shadow_driver.fullscreen_window()
    #     except Exception as err:
    #         print(f"186. fullscreen_window() Exception as {err}")   
                    
    # time.sleep(0.7)
    wait_6 = WebDriverWait(shadow_driver, 6.1) 
    wait_9 = WebDriverWait(shadow_driver, 9.6) 
        
    html_content_visibility(shadow_driver, wait_9, wait_6)
    time.sleep(2.1)
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(2.3)

    html_content_visibility(shadow_driver, wait_9, wait_6)
    time.sleep(2.1)
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(2.3)        
    # time.sleep(9.3)              
    try:
        unavailable_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.unavailable")')         
        if unavailable_button:
            context_driver_read_archive["unavailable_button"] = "yes unavailable_button"
            print("1. YES unavailable_button")
            # shadow_driver.close()

    # except (JavascriptException, NoSuchShadowRootException) as err:
    except JavascriptException as err:        
        print("1. JavascriptException, NoSuchShadowRootException unavailable_button except: { err }")    
        time.sleep(6.1)
        try:
            unavailable_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.unavailable")')         
            if unavailable_button:
                print("2. YES unavailable_button")
                context_driver_read_archive["unavailable_button"] = "yes unavailable_button"
                time.sleep(2.3)

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("2. JavascriptException, NoSuchShadowRootException unavailable_button except: { err }") 
            # context_driver_read_archive["unavailable_button"] = "no unavailable_button" 
            time.sleep(2.1)
            # shadow_driver.close()
            # time.sleep(3.1)
            # shadow_driver.quit()
    
    time.sleep(2.7)
    if context_driver_read_archive["unavailable_button"] == "yes unavailable_button":
        print('1. context_driver_read_archive["unavailable_button"] =', context_driver_read_archive["unavailable_button"])
        time.sleep(2.3)
        archive_title_search = archive_title.replace(" ", "+")
        url_archive = f'https://archive.org/search?query={archive_title_search}&sin=TXT'
        shadow_driver.get(url_archive)
        
        html_content_visibility(shadow_driver, wait_9, wait_6)
        time.sleep(2.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)        
        time.sleep(2.6)
        
        time.sleep(4.2)
        try:
            text_contains = 'a[href*="calibre_library"]'
            # time.sleep(4.2)
            element = shadow.find_element(text_contains)
            # print("element.text = ", element.text)
            book_url = element.get_attribute('href')
            print("1a book_url =", book_url)
            # shadow_driver.close()
            time.sleep(2.3)
            book_url_pdf = book_url.replace("details", "download")[:book_url.index("?q")+1]+".pdf"
            read_archive.link_pdf = book_url_pdf
            context_read_archive["read_archive_link_pdf"] = book_url_pdf         
            try:
                time.sleep(2.3)
                shadow_driver.close()
                time.sleep(3.2)
                shadow_driver.quit()
                return context_read_archive 
            except Exception as err:
                print(f"1. driver_headless except Exception as {err}")            
            
        except Exception as e:
            print(f"722. Exception as {e}")
            time.sleep(9.3)
            try:
                text_contains = 'a[href*="calibre_library"]'
                time.sleep(4.2)
                element = shadow.find_element(text_contains)
                # print("element.text = ", element.text)
                book_url = element.get_attribute('href')
                print("book_url =", book_url)
                # shadow_driver.close()
                time.sleep(2)
                book_url_pdf = book_url.replace("details", "download")[:book_url.index("?q")+1]+".pdf"
                read_archive.link_pdf = book_url_pdf
                context_read_archive["read_archive_link_pdf"] = book_url_pdf
                try:
                    time.sleep(2.3)
                    shadow_driver.close()
                    time.sleep(3.2)
                    shadow_driver.quit()
                    return context_read_archive 
                except Exception as err:
                    print(f"1. driver_headless except Exception as {err}")                  
            except Exception as e:
                print(f"745. Exception as {e}")
                read_archive.return_message = "something went wrong, try another way to find this book"
                context_read_archive["read_archive_return_message"] = "something went wrong, try another way to find this book"
                try:
                    time.sleep(2.3)
                    shadow_driver.close()
                    time.sleep(3.2)
                    shadow_driver.quit()
                    return context_read_archive 
                except Exception as err:
                    print(f"755. driver_headless except Exception as {err}")                  
                             
    # else:
    elif context_driver_read_archive["unavailable_button"] == "unknown":    
        print("759 No unavailable_button")
        html_content_visibility(shadow_driver, wait_9, wait_6)
        time.sleep(2.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)        
        time.sleep(2.6)  
                          
        try:
            return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
            if return_button:
                print("1. yes return_button") 
                context_driver_read_archive["return_button"] = "yes return_button" 
                time.sleep(1.4) 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button)
                except JavascriptException:
                    print("1 JavascriptException return_button")
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button)
                    except JavascriptException:
                        print("1 JavascriptException return_button")                                                      
                                   
        except JavascriptException:
            print("581. JavascriptException element_html")                   
            time.sleep(2.5)
            
            try:
                return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
                if return_button:
                    print("787. yes return_button") 
                    context_driver_read_archive["return_button"] = "yes return_button" 
                    time.sleep(1.4) 
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button)
                    except JavascriptException:
                        print("2 JavascriptException return_button")
                        try:
                            shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button)
                        except JavascriptException:
                            print("2 JavascriptException return_button")
                                    
            except JavascriptException:
                print("446. JavascriptException element_html") 
                # context_driver_read_archive["return_button"] = "no return_button"                   
                time.sleep(2.5)                        
        
        time.sleep(0.6)
        print('805 context_driver_read_archive["return_button"] =', context_driver_read_archive["return_button"])  
        time.sleep(0.6)                               
        # if context_driver_read_archive["return_button"] != "yes return_button":
    if context_driver_read_archive["return_button"] == "unknown":

        try:
            borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
            if borrow_button:
                print("813. YES borrow_button")  
                try:     
                    action.move_to_element(borrow_button)
                    time.sleep(0.5)
                    action.click(borrow_button)
                    action.perform()
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    context_driver_read_archive["borrow_button"] = "click borrow_button"
                    print("821 borrow_button action.click(borrow_button)")
                    time.sleep(0.7)
                    
                except MoveTargetOutOfBoundsException:
                    print("824. MoveTargetOutOfBoundsException borrow_button")
                    time.sleep(2.3) 
                    
                    try:
                        shadow_driver.execute_script("arguments[0].click();", borrow_button)
                        context_driver_read_archive["borrow_button"] = "click borrow_button"
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        print("832 borrow_button arguments[0].click();")
                        time.sleep(0.7)
                    except JavascriptException:
                        print("1. JavascriptException borrow_button click")
                        context_driver_read_archive["borrow_button"] = "no click borrow_button"

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("855. JavascriptException, NoSuchShadowRootException borrow_button except: { err }")  

            try:
                borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
                if borrow_button:
                    print("859. YES borrow_button")
                        
                    try:     
                        action.move_to_element(borrow_button)
                        time.sleep(0.5)
                        action.click(borrow_button)
                        action.perform() 
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        context_driver_read_archive["borrow_button"] = "click borrow_button"
                        time.sleep(0.7)
                        
                    except MoveTargetOutOfBoundsException:
                        print("857. MoveTargetOutOfBoundsException borrow_button")
                        time.sleep(2.3) 
                        try:
                            shadow_driver.execute_script("arguments[0].click();", borrow_button)
                            
                            html_content_visibility(shadow_driver, wait_9, wait_6)
                            context_driver_read_archive["borrow_button"] = "click borrow_button"
                            time.sleep(0.7)
                            
                        except JavascriptException:
                            print("866. JavascriptException borrow_button click")
                            context_driver_read_archive["borrow_button"] = "no click borrow_button"
                            time.sleep(1.4)

            except (JavascriptException, NoSuchShadowRootException) as err:
                print("871. JavascriptException, NoSuchShadowRootException borrow_button except: { err }") 
                time.sleep(0.4) 
                # shadow_driver.close()
                # time.sleep(3.2)
                # shadow_driver.quit()
                
                # read_archive.return_message = "something went wrong, try later or another way to find this book"
                # context_read_archive["read_archive_return_message"] = "something went wrong, try later or another way to find this book"                    
                # return context_read_archive 
                                   

    if context_driver_read_archive["unavailable_button"] == "unknown" and context_driver_read_archive["return_button"] == "unknown" and context_driver_read_archive["borrow_button"] == "unknown":
        html_content_visibility(shadow_driver, wait_9, wait_6)
        print("BUTTONS UNKNOWN")
        html_content_opacity_0(shadow_driver, wait_9, wait_6)
        time.sleep(1.9)
        bars_hidden(shadow_driver, action)
        time.sleep(2.3)    
        html_content_opacity_1(shadow_driver, wait_9, wait_6)
        
        # while True:
        # for i in range(720):
        time.sleep(20)
        current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
        if shadow_driver.current_url != current_book_url:
            try:
                shadow_driver.execute_script("""
                    document.addEventListener('keydown', (event) => {
                        if (event.key == "Escape" || event.code == "Escape") {
                        event.preventDefault();
                        alert(`1. CHANGE SIZE NOT WORKING ;)`);            
                        event.preventDefault();
                    }
                    
            }, false);        
                        
                                """)
            except (JavascriptException, UnexpectedAlertPresentException):
                print("1. JavascriptException escape") 
                   
        # for i in range(9): 
        #     if shadow_driver.current_url != current_book_url:  
        #     try:
        #         shadow_driver.execute_script("""
        #             document.addEventListener('keydown', (event) => {
        #                 if (event.key == "Escape" || event.code == "Escape") {
        #                 event.preventDefault();
        #                 alert(`1. CHANGE SIZE NOT WORKING ;)`);            
        #                 event.preventDefault();
        #             }
                    
        #     }, false);        
                        
        #                         """)
        #     except JavascriptException:
        #         print("JavascriptException escape")
        #     time.sleep(10.0 - ((time.time() - starttime) % 10.0))                                      
                        
        time.sleep(7200)
        # time.sleep(35) 
        try:
            time.sleep(2.3)
            shadow_driver.close()
            time.sleep(3.2)
            shadow_driver.quit()
            context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"    
            print("END READING bars_hidden()")        
            return context_read_archive
        except Exception as err:
            print(f"1. BUTTONS UNKNOWN except Exception as {err}")         
                 
    html_content_visibility(shadow_driver, wait_9, wait_6)
    time.sleep(2.1)
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(5.7)

    try:
        shadow_driver_current_url = shadow_driver.current_url
        print("626 shadow_driver_current_url =", shadow_driver_current_url)
        if shadow_driver_current_url.startswith("https://archive.org/account/login"):
        #url = r"https://archive.org/account/login"
            # shadow_driver.maximize_window()
            # print("563 shadow_driver_current_url =", shadow_driver_current_url)
            # shadow_driver.fullscreen_window()
            context_driver_read_archive["login_url"] = "yes login_url"
            time.sleep(0.3)
            log = ()
            logs = [('booksmart01@hotmail.com', 'Djangoapp01o'), ('booksmart02@hotmail.com', 'Djangoapp02o'), ('booksmart03@hotmail.com', 'Djangoapp03o')]

            random.shuffle(logs)
            log = random.choice(logs)
            print("log =", log)
            time.sleep(1.7)
            # shadow_driver.get(url)
            time.sleep(1.2)             
            try:
                print("storage clear")   
                shadow_driver.execute_script("""
                                    // window.localStorage.clear();
                                    // window.sessionStorage.clear();
                                    
                                    localStorage.clear();
                                    sessionStorage.clear();
                                    """)
            except JavascriptException:
                print("1. JavascriptException")  
        else:                  
            context_driver_read_archive["login_url"] = "no login_url"
    except NoSuchDriverException:
        print("1. NoSuchDriverException login_url")                                          
        context_driver_read_archive["login_url"] = "no login_url"
        
    time.sleep(2.1)     
        
    try:
        if context_driver_read_archive["login_url"] == "yes login_url":
            try:
                username_input = shadow_driver.find_element(By.NAME, "username") 
                if username_input:
                    print("1b. username_input")
                    action.move_to_element(username_input)
                    time.sleep(0.4)
                    action.click(username_input)
                    action.perform()
                    time.sleep(0.3)
                    username_input.send_keys(log[0])
                    
                time.sleep(1.4)   
                
                password_input = shadow_driver.find_element(By.NAME, "password") 
                if password_input:
                    print("1b. password_input")
                    action.move_to_element(password_input)
                    time.sleep(0.5)
                    action.click(password_input)
                    action.perform()
                    time.sleep(0.4)
                    password_input.send_keys(log[1])
                    
                time.sleep(3.9)  
                remember_input = shadow_driver.find_element(By.NAME, "remember")
                if remember_input:
                    print("1b. remember_input")
                    action.move_to_element(remember_input)
                    time.sleep(0.5)
                    action.click(remember_input)
                    action.perform()  
                    
                time.sleep(3.9)          
                submit_btn = shadow_driver.find_element(By.NAME, "submit-to-login")
                if submit_btn:
                    print("1b. submit_btn")
                    try:
                        action.move_to_element(submit_btn)
                        time.sleep(0.4)
                        # action.click(submit_btn)
                        action.perform()
                        time.sleep(0.4)
                        # shadow_driver.minimize_window()
                        shadow_driver.execute_script("arguments[0].click();", submit_btn)
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        time.sleep(0.7)
                        
                    except MoveTargetOutOfBoundsException:
                        print("1000  MoveTargetOutOfBoundsException") 
                        time.sleep(0.9)   
                        try:
                            shadow_driver.execute_script("arguments[0].click();", submit_btn)
                        except JavascriptException:
                            print("1005. submit_btn JavascriptException")
                            time.sleep(0.2)
                            shadow_driver.close()
                            time.sleep(3.1)
                            shadow_driver.quit()
                            
                            context_read_archive["read_archive_return_message"] = "something went wrong, try another way to find this book"
                            read_archive.return_message = "something went wrong, try another way to find this book"                          
                            return context_read_archive
                            
                    # time.sleep(0.4) 
                    # shadow_driver.minimize_window() 
            except NoSuchElementException:
                print("1. username_input") 
                
                try:
                    username_input = shadow_driver.find_element(By.NAME, "username") 
                    if username_input:
                        print("1b. username_input")
                        action.move_to_element(username_input)
                        time.sleep(0.4)
                        action.click(username_input)
                        action.perform()
                        time.sleep(0.3)
                        username_input.send_keys(log[0])
                        
                    time.sleep(1.4)   
                    
                    password_input = shadow_driver.find_element(By.NAME, "password") 
                    if password_input:
                        print("1b. password_input")
                        action.move_to_element(password_input)
                        time.sleep(0.5)
                        action.click(password_input)
                        action.perform()
                        time.sleep(0.4)
                        password_input.send_keys(log[1])
                        
                    time.sleep(3.9)  
                    remember_input = shadow_driver.find_element(By.NAME, "remember")
                    if remember_input:
                        action.move_to_element(remember_input)
                        time.sleep(0.5)
                        action.click(remember_input)
                        action.perform()  
                        
                    time.sleep(3.9)          
                    submit_btn = shadow_driver.find_element(By.NAME, "submit-to-login")
                    if submit_btn:
                        print("1b. submit_btn")
                        try:
                            action.move_to_element(submit_btn)
                            time.sleep(0.4)
                            action.click(submit_btn)
                            action.perform()
                            html_content_visibility(shadow_driver, wait_9, wait_6)
                            time.sleep(0.7)
                            
                        except MoveTargetOutOfBoundsException:
                            print("1064  MoveTargetOutOfBoundsException") 
                            time.sleep(0.9)   
                            try:
                                shadow_driver.execute_script("arguments[0].click();", submit_btn)
                            except JavascriptException:
                                print("627. submit_btn JavascriptException")
                                time.sleep(0.2)
                                shadow_driver.close()
                                time.sleep(3.1)
                                shadow_driver.quit()
                                
                                context_read_archive["read_archive_return_message"] = "something went wrong, try another way to find this book"
                                read_archive.return_message = "something went wrong, try another way to find this book"                                  
                                
                                return context_read_archive
                except NoSuchElementException:
                    print("2. username_input")                         
    except Exception as err:
        print(f"1082 login Exception as {err}")                        

    html_content_visibility(shadow_driver, wait_9, wait_6)
    time.sleep(3.1)
    # shadow_driver.maximize_window()
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(2.3)

    try:
        shadow_driver_current_url_book_first = shadow_driver.current_url
        print("1087 shadow_driver_current_url_book_first =", shadow_driver_current_url_book_first)    
    except Exception as err:
        print(f"1089 shadow_driver_current_url_book_first Exception as {err}")
            
    time.sleep(5.6)
    try:
        html_content_visibility(shadow_driver, wait_9, wait_6)
        print("1099. html_content_visibility(shadow_driver, wait_9, wait_6)")
        time.sleep(3.1)
        # shadow_driver.maximize_window()
        html_content_opacity_0(shadow_driver, wait_9, wait_6)
        time.sleep(2.3)        
        borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
        if borrow_button:
            print("1095. YES borrow_button")  
            try:
                borrow_button_text = borrow_button.text
                if borrow_button_text == "Log In and Borrow":
                    print('1100. borrow_button_text == "Log In and Borrow"')
                    time.sleep(10.3)
                    shadow_driver.close()
                    time.sleep(3.2)
                    shadow_driver.quit()
                    
                    read_archive.return_message = "something went wrong, try later or another way to find this book"
                    context_read_archive["read_archive_return_message"] = "something went wrong, try later or another way to find this book"                    
                    return context_read_archive
            except Exception as err:
                print(f"1110 borrow_button_text Exception as {err}")
            
            time.sleep(0.9)                    
            try:     
                action.move_to_element(borrow_button)
                time.sleep(0.5)
                # action.click(borrow_button)
                action.perform()
                time.sleep(0.7)
                shadow_driver.execute_script("arguments[0].click();", borrow_button)
                html_content_visibility(shadow_driver, wait_9, wait_6)
                context_driver_read_archive["borrow_button"] = "click borrow_button"
                print("1122. borrow_button click")
                time.sleep(0.7)
                
            except MoveTargetOutOfBoundsException:
                print("1125. MoveTargetOutOfBoundsException borrow_button")
                time.sleep(2.3) 
                try:
                    shadow_driver.execute_script("arguments[0].click();", borrow_button)
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    context_driver_read_archive["borrow_button"] = "click borrow_button"
                    print("1132. borrow_button click")
                    time.sleep(0.7)
                    
                except JavascriptException:
                    print("800. JavascriptException borrow_button click")
                    context_driver_read_archive["borrow_button"] = "no click borrow_button"

    # except (JavascriptException, NoSuchShadowRootException) as err:
    except (JavascriptException, NoSuchShadowRootException) as err:
        print("1. JavascriptException, NoSuchShadowRootException borrow_button except: { err }")  

        time.sleep(3.5)                
        try:
            borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
            if borrow_button:
                print("888. YES borrow_button")  
                try:
                    borrow_button_text = borrow_button.text
                    if borrow_button_text == "Log In and Borrow":
                        print('borrow_button_text == "Log In and Borrow"')
                        time.sleep(10.3)
                        shadow_driver.close()
                        time.sleep(3.2)
                        shadow_driver.quit()
                        read_archive.return_message = "something went wrong, try later or another way to find this book"
                        context_read_archive["read_archive_return_message"] = "something went wrong, try later or another way to find this book"                    
                        return context_read_archive
                except Exception as err:
                    print(f"901 borrow_button_text Exception as {err}")
                
                time.sleep(0.9)   
                try:     
                    action.move_to_element(borrow_button)
                    time.sleep(0.5)
                    action.click(borrow_button)
                    action.perform()  
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    context_driver_read_archive["borrow_button"] = "click borrow_button"
                    time.sleep(0.7)
                    
                except MoveTargetOutOfBoundsException:
                    print("1. MoveTargetOutOfBoundsException borrow_button")
                    time.sleep(2.3) 
                    try:
                        shadow_driver.execute_script("arguments[0].click();", borrow_button)
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        context_driver_read_archive["borrow_button"] = "click borrow_button"
                        time.sleep(0.7)
                        
                    except JavascriptException:
                        print("1. JavascriptException borrow_button click")
                        context_driver_read_archive["borrow_button"] = "no click borrow_button"

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("782. JavascriptException, NoSuchShadowRootException borrow_button except: { err }") 
            shadow_driver.close()
            time.sleep(2.8)
            shadow_driver.quit()
            
            read_archive.return_message = "something went wrong, try later or another way to find this book"
            context_read_archive["read_archive_return_message"] = "something went wrong, try later or another way to find this book"                    
            return context_read_archive
                        
    # try:
    #     shadow_driver.fullscreen_window()
    # except Exception as err:
    #     print(f"788. fullscreen_window() Exception as {err}") 
    #     time.sleep(0.6)
    #     try:
    #         shadow_driver.fullscreen_window()
    #     except Exception as err:
    #         print(f"793. fullscreen_window() Exception as {err}") 
    
    html_content_visibility(shadow_driver, wait_9, wait_6)
    print("1205  html_content_visibility(shadow_driver, wait_9, wait_6)")
    time.sleep(3.1)
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(3.4)     

    # time.sleep(15.3)  
    # print("899 try return_button") 
    # time.sleep(0.9)
    # try:
    #     return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
        
    #     if return_button:
    #         print("905. YES return_button") 
                      

    # except JavascriptException as err:
    #     print("905a. JavascriptException, NoSuchShadowRootException return_button except: { err }")     
    #     time.sleep(6.3)
    #     try:
    #         return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
    #         if return_button:
    #             print("905a. YES return_button") 
                       
    #     except (JavascriptException, NoSuchShadowRootException) as err:
    #         print("905a. JavascriptException, NoSuchShadowRootException return_button except: { err }")

    # html_content_visibility(shadow_driver, wait_9, wait_6)    
    # time.sleep(2.1)
    # html_content_opacity_0(shadow_driver, wait_9, wait_6)
    # time.sleep(2.3)
           
    try:
        html_content_visibility(shadow_driver, wait_9, wait_6)
        print("1243  html_content_visibility(shadow_driver, wait_9, wait_6)")
        time.sleep(3.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)    
        time.sleep(2.9)   
        print("1247. try return_button_bar")  
        return_button_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div")')
        
        if return_button_bar:
            print("1243. YES return_button_bar") 
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
            except JavascriptException:
                print("1247. JavascriptException return_button_bar")
                
                time.sleep(2.6)
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                except JavascriptException:
                    print("1253. JavascriptException return_button_bar")                         

    except JavascriptException as err:
        print("1256. JavascriptException, NoSuchShadowRootException return_button_bar except: { err }")     
        html_content_visibility(shadow_driver, wait_9, wait_6)
        time.sleep(3.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)    
        time.sleep(2.9) 
        try:
            return_button_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
            if return_button_bar:
                print("1261. YES return_button_bar") 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                except JavascriptException:
                    print("960a JavascriptException return_button_bar") 
                    time.sleep(2.6)
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                    except JavascriptException:
                        print("960a JavascriptException return_button_bar")                            

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("1273. JavascriptException, NoSuchShadowRootException return_button_bar except: { err }")
            html_content_visibility(shadow_driver, wait_9, wait_6)
            time.sleep(3.1)
            html_content_opacity_0(shadow_driver, wait_9, wait_6)    
            time.sleep(2.9)             

    time.sleep(0.8)
    # document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > info-icon")

    bars_hidden(shadow_driver, action)
    time.sleep(4.3)    
    # shadow_driver.maximize_window()
    # time.sleep(0.3)
    # shadow_driver.fullscreen_window() 
    # time.sleep(7.4)  

    
    print("1. book_reader.current_url =", shadow_driver.current_url)
    time.sleep(2.1)
    html_content_opacity_1(shadow_driver, wait_9, wait_6)
    time.sleep(2.3)

    time.sleep(20)
    current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
    if shadow_driver.current_url != current_book_url:
        try:
            shadow_driver.execute_script("""
                document.addEventListener('keydown', (event) => {
                    if (event.key == "Escape" || event.code == "Escape") {
                    event.preventDefault();
                    alert(`2. CHANGE SIZE NOT WORKING ;)`);            
                    event.preventDefault();
                }
                
            }, false);        
                            """)
        except (JavascriptException, UnexpectedAlertPresentException):
            print("JavascriptException escape")     
                        
    # time.sleep(3500)
    # while True:
    # for i in range(350):
    # for i in range(9):    
    #     try:
    #         shadow_driver.execute_script("""
    #             document.addEventListener('keydown', (event) => {
    #             if (event.key == "Escape" || event.code == "Escape") {
    #                 event.preventDefault();
    #                 alert(` CHANGE SIZE NOT WORKING ;)`);            
    #                 event.preventDefault();
    #             }
                
    #     }, false);        
                    
    #                         """)
    #     except JavascriptException:
    #         print("JavascriptException escape")
    #     time.sleep(10.0 - ((time.time() - starttime) % 10.0)) 
    
    time.sleep(3500)            
    # time.sleep(35)
    print("\nFIRST RETURN\n")
    # shadow_driver_current_url_book = shadow_driver._configure_headless
    print("1275 shadow_driver.current_url =", shadow_driver.current_url)
    time.sleep(1.6)
    try:
        return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
        if return_button:
            print("1378. YES return_button") 
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'visible'", return_button)
            except JavascriptException:
                print("1378 JavascriptException return_button")        
            try:                                
                action.move_to_element(return_button)
                time.sleep(0.5)
                # action.click(return_button)
                action.perform()
                shadow_driver.execute_script("arguments[0].click();", return_button)
                html_content_visibility(shadow_driver, wait_9, wait_6)
                print("1307 action.click(return_button)")
                time.sleep(0.7)
                
            except MoveTargetOutOfBoundsException:
                print("1378. MoveTargetOutOfBoundsException return_button")
                time.sleep(1.5)
                try:                                
                    shadow_driver.execute_script("arguments[0].click();", return_button)
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    print("1322 action.click(return_button)")
                    time.sleep(0.7)
                    # shadow_driver.minimize_window()
                    
                except JavascriptException:
                    print("1327. JavascriptException return_button")
                    time.sleep(1.5)   
    except JavascriptException as err:
        print("1378a. JavascriptException, NoSuchShadowRootException return_button except: { err }")     
        time.sleep(2.3)
        try:
            return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
            if return_button:
                print("1404. YES return_button") 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'visible'", return_button)
                except JavascriptException:
                    print("1404. JavascriptException return_button")        
                try:                                
                    action.move_to_element(return_button)
                    time.sleep(0.5)
                    # action.click(return_button)
                    action.perform()
                    shadow_driver.execute_script("arguments[0].click();", return_button)
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    time.sleep(0.7)
                   
                except MoveTargetOutOfBoundsException:
                    print("1404. MoveTargetOutOfBoundsException return_button")
                    time.sleep(1.5)
                    try:                                
                        shadow_driver.execute_script("arguments[0].click();", return_button)
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        time.sleep(0.7)
                        # shadow_driver.minimize_window()

                    except JavascriptException:
                        print("1404. JavascriptException return_button")
                        time.sleep(1.5)   
        except (JavascriptException, NoSuchShadowRootException) as err:
            print("1404. JavascriptException, NoSuchShadowRootException return_button except: { err }")
    
    # try:
    #     shadow_driver.fullscreen_window()
    # except Exception as err:
    #     print(f"1205. fullscreen_window() Exception as {err}") 
    #     time.sleep(0.6)
    #     try:
    #         shadow_driver.fullscreen_window()
    #     except Exception as err:
    #         print(f"1210. fullscreen_window() Exception as {err}") 
    
    html_content_visibility(shadow_driver, wait_9, wait_6)        
    time.sleep(3.4)        
    html_content_opacity_0(shadow_driver, wait_9, wait_6)
    time.sleep(4.3)                
    try:
        html_content_visibility(shadow_driver, wait_9, wait_6)
        print("1388  html_content_visibility(shadow_driver, wait_9, wait_6)")
        time.sleep(3.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)    
        time.sleep(2.9)           
        borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
        if borrow_button:
            print("1394. YES borrow_button")  
            try:     
                action.move_to_element(borrow_button)
                time.sleep(0.5)
                # action.click(borrow_button)
                action.perform()
                time.sleep(0.6)
                shadow_driver.execute_script("arguments[0].click();", borrow_button)
                html_content_visibility(shadow_driver, wait_9, wait_6)
                time.sleep(0.7) 
            except MoveTargetOutOfBoundsException:
                print("1477. MoveTargetOutOfBoundsException borrow_button")
                time.sleep(2.3) 
                try:
                    shadow_driver.execute_script("arguments[0].click();", borrow_button)
                    html_content_visibility(shadow_driver, wait_9, wait_6)
                    time.sleep(0.7) 
                except JavascriptException:
                    print("1477. JavascriptException borrow_button click")
            

    except (JavascriptException, NoSuchShadowRootException) as err:
        print("1973. JavascriptException, NoSuchShadowRootException borrow_button except: { err }")
        
        time.sleep(3.1)                              
        try:
            borrow_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.primary.initial")')
            if borrow_button:
                print("1499. YES borrow_button")  
                try:     
                    action.move_to_element(borrow_button)
                    time.sleep(0.5)
                    action.click(borrow_button)
                    action.perform()
                    html_content_visibility(shadow_driver, wait_9, wait_6)  
                    time.sleep(0.7) 
                except MoveTargetOutOfBoundsException:
                    print("1499. MoveTargetOutOfBoundsException borrow_button")
                    time.sleep(2.3) 
                    try:
                        shadow_driver.execute_script("arguments[0].click();", borrow_button)
                        html_content_visibility(shadow_driver, wait_9, wait_6)
                        time.sleep(0.4) 
                    except JavascriptException:
                        print("1499. JavascriptException borrow_button click")
                
        except (JavascriptException, NoSuchShadowRootException) as err:
            print("1499. JavascriptException, NoSuchShadowRootException borrow_button except: { err }")

    html_content_visibility(shadow_driver, wait_9, wait_6)
    time.sleep(3.4) 
    html_content_opacity_0(shadow_driver, wait_9, wait_6)

    # time.sleep(15.3)  
    # print("1351 try return_button") 
    # time.sleep(0.9)
    # try:
    #     return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
        
    #     if return_button:
    #         context_driver_read_archive["return_button"] = "yes return_button"  
    #         time.sleep(0.9)
    #         print("1657. YES return_button_bar") 
    #         time.sleep(0.9)
                      
    # except JavascriptException as err:
    #     print("1557a. JavascriptException, NoSuchShadowRootException return_button except: { err }")     
    #     time.sleep(6.3)
    #     try:
    #         return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
    #         if return_button:
    #             context_driver_read_archive["return_button"] = "yes return_button"  
    #             time.sleep(0.9)
    #             print("1657a. YES return_button")
    #             time.sleep(0.9) 
                       

    #     except (JavascriptException, NoSuchShadowRootException) as err:
    #         print("1657a. JavascriptException, NoSuchShadowRootException return_button except: { err }")

    # html_content_visibility(shadow_driver, wait_9, wait_6)   
    # time.sleep(3.5)         
    # html_content_opacity_0(shadow_driver, wait_9, wait_6)
    # time.sleep(2.3)       
            
    time.sleep(4.7)          
    try:
        html_content_visibility(shadow_driver, wait_9, wait_6)
        print("1477  html_content_visibility(shadow_driver, wait_9, wait_6)")
        time.sleep(3.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)    
        time.sleep(2.9)   
        print("1489. try return_button_bar")  
        return_button_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div")')
        
        if return_button_bar:
            print("1464. YES return_button_bar_bar") 
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
            except JavascriptException:
                print("1744. JavascriptException return_button_bar")
                
                time.sleep(2.6)
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                except JavascriptException:
                    print("1744. JavascriptException return_button_bar")                         

    except JavascriptException as err:
        print("1614. JavascriptException, NoSuchShadowRootException return_button_bar except: { err }")     
        html_content_visibility(shadow_driver, wait_9, wait_6)
        time.sleep(3.1)
        html_content_opacity_0(shadow_driver, wait_9, wait_6)    
        time.sleep(2.9) 
        try:
            return_button_bar = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
            if return_button_bar:
                print("1764a. YES return_button_bar") 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                except JavascriptException:
                    print("1764a JavascriptException return_button_bar") 
                    time.sleep(2.6)
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", return_button_bar)
                    except JavascriptException:
                        print("1764a JavascriptException return_button_bar")                            

        except (JavascriptException, NoSuchShadowRootException) as err:
            print("1764a. JavascriptException, NoSuchShadowRootException return_button_bar except: { err }")
            html_content_visibility(shadow_driver, wait_9, wait_6)
            time.sleep(3.1)
            html_content_opacity_0(shadow_driver, wait_9, wait_6)    
            time.sleep(2.9)             
            
    time.sleep(4.1)
    bars_hidden(shadow_driver, action)

    time.sleep(4.3)    
    # shadow_driver.maximize_window()
    # time.sleep(0.3)
    # shadow_driver.fullscreen_window() 
    # time.sleep(7.4)  

    
    print("1626. book_reader.current_url =", shadow_driver.current_url)
    time.sleep(2.7)                
    html_content_opacity_1(shadow_driver, wait_9, wait_6)
    time.sleep(2.3)
    time.sleep(20)    
    current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
    if shadow_driver.current_url != current_book_url:
        try:
            shadow_driver.execute_script("""
                document.addEventListener('keydown', (event) => {
                    if (event.key == "Escape" || event.code == "Escape") {
                    event.preventDefault();
                    alert(`3. CHANGE SIZE NOT WORKING ;)`);            
                    event.preventDefault();
                }
                
        });        
                    
                            """)
        except (JavascriptException, UnexpectedAlertPresentException):
            print("JavascriptException escape")                    
    # time.sleep(3500)
    # time.sleep(95)
    # while True:
    # for i in range(350):
    # for i in range(9):    
    #     try:
    #         shadow_driver.execute_script("""
    #             document.addEventListener('keydown', (event) => {
    #             if (event.key == "Escape" || event.code == "Escape") {
    #                 event.preventDefault();
    #                 alert(`1. CHANGE SIZE NOT WORKING ;)`);            
    #                 event.preventDefault();
    #             }
                
    #     }, false);        
                    
    #                         """)
    #     except JavascriptException:
    #         print("JavascriptException escape")
    #     time.sleep(10.0 - ((time.time() - starttime) % 10.0)) 
        
    # print("\nLAST RETURN\n")
    # time.sleep(2.8)
    
    time.sleep(3500)
    # time.sleep(35)
    try:
        return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
        if return_button:
            print("1545. YES return_button") 
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'visible'", return_button)
            except JavascriptException:
                print("JavascriptException return_button")        
            try:                                
                action.move_to_element(return_button)
                time.sleep(0.5)
                action.click(return_button)
                action.perform()
                print("1555 1. END borrow")
                time.sleep(0.2)
                shadow_driver.close()
                time.sleep(3.1)
                shadow_driver.quit()
                
                context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
                read_archive.return_message = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"                          
                return context_read_archive
            except MoveTargetOutOfBoundsException:
                print("1565. MoveTargetOutOfBoundsException return_button")
                time.sleep(1.5)
                try:                                
                    shadow_driver.execute_script("arguments[0].click();", return_button)
                    # shadow_driver.minimize_window()
                    print("1570  END borrow")
                    time.sleep(0.2)
                    shadow_driver.close()
                    time.sleep(3.1)
                    shadow_driver.quit()
                    
                    context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
                    read_archive.return_message = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"                          
                    return context_read_archive
                except JavascriptException:
                    print("2025 JavascriptException return_button")
                    time.sleep(1.5)   
    except (JavascriptException, NoSuchShadowRootException) as err:
        print("2025a. JavascriptException, NoSuchShadowRootException return_button except: { err }")     
        time.sleep(2.3)
        try:
            return_button = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div > section.action-buttons.primary > button.ia-button.danger.initial")')
            if return_button:
                print("2025a. YES return_button") 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'visible'", return_button)
                except JavascriptException:
                    print("2025a JavascriptException return_button")        
                try:                                
                    action.move_to_element(return_button)
                    time.sleep(0.5)
                    action.click(return_button)
                    action.perform()
                    print("3. END borrow")
                    time.sleep(0.2)
                    shadow_driver.close()
                    time.sleep(3.1)
                    shadow_driver.quit()
                    
                    context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
                    read_archive.return_message = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"                          
                    return context_read_archive                 
                except MoveTargetOutOfBoundsException:
                    print("2053 MoveTargetOutOfBoundsException return_button")
                    time.sleep(1.5)
                    try:                                
                        shadow_driver.execute_script("arguments[0].click();", return_button)
                        print("2053 4. END borrow")
                        time.sleep(0.2)
                        shadow_driver.close()
                        time.sleep(3.1)
                        shadow_driver.quit()
                        
                        context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
                        read_archive.return_message = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"                          
                        return context_read_archive
                    except JavascriptException:
                        print("2053 JavascriptException return_button")
                        time.sleep(1.5)   
        except (JavascriptException, NoSuchShadowRootException) as err:
            print("2053a. JavascriptException, NoSuchShadowRootException return_button except: { err }")
            print("2053a 5. END borrow")
            time.sleep(0.2)
            shadow_driver.close()
            time.sleep(3.1)
            shadow_driver.quit()
            
            context_read_archive["read_archive_return_message"] = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
            read_archive.return_message = "END READING IF YOU WISH YOU CAN BORROW THIS BOOK AGAIN"
            return context_read_archive        