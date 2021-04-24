from selenium import webdriver
from time import sleep
import pickle
import traceback
import asyncio
from pyppeteer import launch
from selenium.webdriver import ChromeOptions

option__ = ChromeOptions()
option__.add_experimental_option('excludeSwitches', ['enable-automation'])

# driver = webdriver.Firefox(r"E:\43j6ugol.d")
driver = webdriver.Chrome(options=option__)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
        })
driver.get("https://m.polyt.cn/login?redirect=%2Fmine")

sleep(40)
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# try:
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         print(cookie)
#         new_cookie = {}
#         new_cookie['name'] = cookie['name']
#         new_cookie['value'] = cookie['value']
#         driver.add_cookie(new_cookie)
# except:
#     traceback.print_exc()
