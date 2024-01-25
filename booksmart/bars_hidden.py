    try:
        # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button")
        fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
        if fullscreen_button:
            print("1751. YES fullscreen_button") 
            try:     
                action.move_to_element(fullscreen_button)
                time.sleep(0.5)
                action.click(fullscreen_button)
                action.perform()  
            except MoveTargetOutOfBoundsException:
                print("1751. MoveTargetOutOfBoundsException borrow_button")
                time.sleep(2.3)        
                try:     
                    shadow_driver.execute_script("arguments[0].click();", fullscreen_button)
                except JavascriptException:
                    print("1764. JavascriptException borrow_button")
                    time.sleep(2.3)   
                    
    except NoSuchElementException:
        print("1791. NO fullscreen_button")   
        time.sleep(2.9) 
        
        try:
            # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button") 
            # fullscreen_button = shadow_driver.execute_script('return document.querySelector("#BookReader > div.BRfooter > div > nav > ul > li:nth-child(10) > button")') 
            fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
            if fullscreen_button:
                print("1805. YES fullscreen_button")  
                        
                try:     
                    action.move_to_element(fullscreen_button)
                    time.sleep(0.5)
                    action.click(fullscreen_button)
                    action.perform()  
                    time.sleep(2.1)  
                    # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
                    # shadow_driver.get(current_book_url)
                except MoveTargetOutOfBoundsException:
                    print("1805. MoveTargetOutOfBoundsException fullscreen_button")
                    time.sleep(2.3)        
                    try:     
                        shadow_driver.execute_script("arguments[0].click();", fullscreen_button)
                        time.sleep(2.1)  
                        # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
                        # shadow_driver.get(current_book_url)
                    except JavascriptException:
                        print("1806. JavascriptException fullscreen_button")
                        time.sleep(2.3)  
                        
        except JavascriptException:
            print("1826. NO fullscreen_button")
            time.sleep(3.9)  
            # current_book_url = f'https://archive.org/details/{link_id}/mode/2up?view=theater'
            # shadow_driver.get(current_book_url)
            # time.sleep(7.9)     
    time.sleep(2.7)        
    try:
        # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button")
        fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
        if fullscreen_button:
            print("1706. YES fullscreen_button") 
                   
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                print("1706 yes hidden lfullscreen_button")
            except JavascriptException:
                print("1706. JavascriptException fullscreen_button hidden")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                    print("1706. yes hidden lfullscreen_button")
                except JavascriptException:
                    print("1706 JavascriptException fullscreen_button hidden")
                    
    except NoSuchElementException:
        print("1706. NO fullscreen_button")   
        time.sleep(2.9) 
        
        try:
            # fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(10) > button") 
            # fullscreen_button = shadow_driver.execute_script('return document.querySelector("#BookReader > div.BRfooter > div > nav > ul > li:nth-child(10) > button")') 
            fullscreen_button = shadow_driver.find_element(By.CSS_SELECTOR, "#BookReader > div.BRfooter > div > nav > ul.controls > li:nth-child(11) > button") 
            if fullscreen_button:
                print("1860. YES fullscreen_button")  
                        
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                    print("1860 yes hidden fullscreen_button")
                except JavascriptException:
                    print("1860. JavascriptException fullscreen_button hidden")
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", fullscreen_button)
                        print("1860a yes hidden fullscreen_button")
                    except JavascriptException:
                        print("1860a JavascriptException fullscreen_button hidden")
                        
        except JavascriptException:
            print("1860 NO fullscreen_button")   
            time.sleep(3.9)  

    time.sleep(3.7)
    print("shadow_driver.execute_script event.key")
    time.sleep(2.3)
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
                var_mymodal_pd();
                }
                if (code_3 === "F12") {
                event.preventDefault();
                alert(` INSEPECT IS NOT WORKING ;)`);
                }  
                if (code_3 === "Escape") {
                    event.preventDefault();
                    alert(` CHANGE SIZE NOT WORKING ;)`);
                }
                
                if (code_3 === "F11") {
                    event.preventDefault();
                    alert(` CHANGE SIZE NOT WORKING ;)`);
                }
                
            }, false);                      
                                """)
    except JavascriptException:
        print("1801. JavascriptException")
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
                    
    # time.sleep(2.3)                    
    # try:
    #     html_content = (By.CSS_SELECTOR, "html")
    #     element_html = wait_9.until(EC.presence_of_element_located(html_content))
    #     if element_html:
    #         print("1 YES element_html")
    #         try:
    #             shadow_driver.execute_script("arguments[0].style.opacity = '0.2';", element_html)
    #         except JavascriptException:
    #             print("1. JavascriptException opacity")    
    #             time.sleep(0.4)
    #             try:
    #                 shadow_driver.execute_script("arguments[0].style.opacity = '0.2';", element_html)
    #             except JavascriptException:
    #                 print("1. JavascriptException opacity")  
    # except TimeoutException:
    #     print("1 TimeoutException element_html")   
    #     time.sleep(1.6)
    #     try:
    #         html_content = (By.CSS_SELECTOR, "html")
    #         element_html = wait_9.until(EC.presence_of_element_located(html_content))
    #         if element_html:
    #             print("1a YES element_html")
    #             try:
    #                 shadow_driver.execute_script("arguments[0].style.opacity = '0.2';", element_html)
    #             except JavascriptException:
    #                 print("1a. JavascriptException opacity")    
    #                 time.sleep(0.4)
    #                 try:
    #                     shadow_driver.execute_script("arguments[0].style.opacity = '0.2';", element_html)
    #                 except JavascriptException:
    #                     print("1a. JavascriptException opacity")  
    #     except TimeoutException:
    #         print("1a TimeoutException element_html")                       
    time.sleep(4.1)          
    try:
        actiongroup = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div.actiongroup")')
        if actiongroup:
            print("1989. YES actiongroup")
            try:
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                
            except JavascriptException:
                print("1989. JavascriptException")  
                time.sleep(3.2) 
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                    
                except JavascriptException:
                    print("1989. JavascriptException")  
                    time.sleep(3.2)                     
        
    except JavascriptException:
        print("1959. NO actiongroup")  

        time.sleep(4.5)
        try:
            actiongroup = shadow_driver.execute_script('return document.querySelector("#IABookReaderMessageWrapper > ia-book-actions").shadowRoot.querySelector("section > collapsible-action-group").shadowRoot.querySelector("div.actiongroup")')
            if actiongroup:
                print("2010a. YES actiongroup")
                try:
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                    
                except JavascriptException:
                    print("2010a. JavascriptException")  
                    time.sleep(3.2) 
                    try:
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", actiongroup)
                        
                    except JavascriptException:
                        print("2010a. JavascriptException")  
                        time.sleep(3.2)                     
            
        except JavascriptException:
            print("2010a. NO actiongroup")   
            
    # time.sleep(1.4)    
    # shadow_driver.maximize_window()
    # time.sleep(0.3)
    # shadow_driver.fullscreen_window()
    time.sleep(1.4)      
    try:
        left_buttons = shadow_driver.execute_script('return document.querySelector("#theatre-ia > div.row > div > ia-book-theater").shadowRoot.querySelector("ia-bookreader").shadowRoot.querySelector("div > iaux-item-navigator").shadowRoot.querySelector("#frame > div > nav > div.minimized")')
        if left_buttons:
            print("2035. YES left_buttons")
            try: 
                shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                print("2035. yes hidden left_buttons")
            except JavascriptException:
                print("2035. no hidden left_buttons")
                try: 
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                    print("2035. yes hidden left_buttons")
                except JavascriptException:
                    print("2035 no hidden left_buttons")                
                                
    # except NoSuchElementException:
    except JavascriptException as err:
        print("2050. JavascriptException, NoSuchShadowRootException left_buttons except: { err }") 
        print("2050.. NO left_buttons") 
        time.sleep(3.1)                
        try:
            left_buttons = shadow_driver.execute_script('return document.querySelector("#theatre-ia > div.row > div > ia-book-theater").shadowRoot.querySelector("ia-bookreader").shadowRoot.querySelector("div > iaux-item-navigator").shadowRoot.querySelector("#frame > div > nav > div.minimized")')
            if left_buttons:
                print("2050.. YES left_buttons")

                try: 
                    shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                    print("2050. yes hidden left_buttons")
                except JavascriptException:
                    print("2050. no hidden left_buttons")
                    try: 
                        shadow_driver.execute_script("arguments[0].style.visibility = 'hidden'", left_buttons)
                        print("2050. yes hidden left_buttons")
                    except JavascriptException:
                        print("2050. no hidden left_buttons")                    
                                
    # except NoSuchElementException:
        except (JavascriptException, NoSuchShadowRootException) as err:
            print("2a. JavascriptException, NoSuchShadowRootException left_buttons except: { err }") 