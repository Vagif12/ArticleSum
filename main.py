from selenium import webdriver
import time
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from fastapi import FastAPI, Request

app = FastAPI()


display = Display(visible=0, size=(800, 600))
display.start()


chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("load-extension=./ext")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 45)
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
print(driver.find_element_by_class_name('sc-gsDKAQ').text
)
gbutton = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.sc-gsDKAQ')))
gbutton.click()

password = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.sc-dJjYzT '))).send_keys("leine.tee1@gmail.com")
password2 = wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//input[@type="password"]'))).send_keys("Penguin12!!")

time.sleep(0.5)
done = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.sc-dlVxhl'))).click()

def main(url):
    driver.execute_script(f"window.open('{url}');")   
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[2])
    # btn = wait.until(EC.visibility_of_element_located(
    # (By.CSS_SELECTOR, '.App_visible__3AYQf')))
    # hover = ActionChains(driver).move_to_element(btn)
    # hover.perform()
    # time.sleep(1.5)
    btn2 = ''
    if driver.current_url != url:
        driver.get(url)
    else:
        driver.get(driver.current_url)
    try:
        btn2 = WebDriverWait(driver,10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.App_visible__3AYQf')))
    except:
        return "This website is currently not supported by this model. Please try a different model!"
    hover = ActionChains(driver).move_to_element(btn2).perform()
    btn3 = wait.until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '.App_visible__3AYQf'))).click()
    # hover.perform()

    try:
        title1 = WebDriverWait(driver,4).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SummaryContent_title__1E08m')))
        content1 = WebDriverWait(driver,4).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SummaryContent_content__6YxH6')))
        return title1.text,content1.text
    except:
        content4 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SummaryContent_content__6YxH6')))
        title4 = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.SummaryContent_title__1E08m')))
        return title4.text,content4.text

@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    url = data['url']
    result = None
    while result is None:
        try:
            # connect
            result = main(url)
            if result != "This website is currently not supported by this model. Please try a different model!":
                result = '\n'.join(result)
                result = result.replace('\nHow was this summary?\nSummari Inc | © Copyright 2022','')
                result = result.replace('\n','\n\n')
            return {"output":result}
        except Exception as e:
            if 'unexpected token' in e:
                return {"output":e}
            else:
                pass
