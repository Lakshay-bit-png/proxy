def trending_topics():
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import ProxyMeshh
    import time
    import requests
    import random
    from webdriver_manager.chrome import ChromeDriverManager
    

    # List of proxies to choose from
    proxi = [random.choice(ProxyMeshh.config)]


    # Function to test if a proxy works
    def test_proxy(proxy):
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}',
        }
        try:
            response = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
            if response.status_code == 200:
                return True
        except Exception as e:
            print(f"Proxy {proxy} failed: {e}")
        return False

    working_proxy = None
    for proxy in proxi:
        if test_proxy(proxy):
            working_proxy = proxy
            break

    if not working_proxy:
        print("No working proxy found")
        exit(1)

    print(f"Using proxy: {working_proxy}")
    
    chrome_options = webdriver.ChromeOptions()
    '''chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")'''
    chrome_options.add_argument(f'--proxy-server={working_proxy}')
     
    
    driver = webdriver.Chrome()

    wait = WebDriverWait(driver, 20)  # Increased the wait time to 20 seconds
    try:
        
        driver.get('https://twitter.com/login')
        
        time.sleep(8) 
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="text"]')))
        username_input.send_keys('TestLaksha15220')

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Next"]/..')))
        next_button.click()

        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
        password_input.send_keys('patlamayadevam')

        password_input.send_keys(Keys.RETURN)

        wait.until(EC.presence_of_element_located((By.XPATH, '//nav')))

        driver.get('https://twitter.com/home')
        time.sleep(10)  
        whats_happening_section = wait.until(EC.presence_of_element_located((By.XPATH, '//section[@aria-labelledby="accessible-list-0"]')))

        trending_topics = whats_happening_section.find_elements(By.XPATH, './/div[@data-testid="trend"]')[:5]

        L=[working_proxy]
        for index, topic in enumerate(trending_topics, start=1):
            topic_text = topic.text
            L.append(topic_text)
        print("main code - - ")
        print(L)
        return L

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the browser
        driver.quit()
