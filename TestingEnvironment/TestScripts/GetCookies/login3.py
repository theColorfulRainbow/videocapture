'''
How to add cookies to open session/driver/browser
Issue: Sometimes it doesn't automatically log me in...not sure why
'''
import time
import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url1 = 'https://echo360.org.uk/directLogin'
url2 = 'https://echo360.org.uk'

options = Options()
options.add_argument('--headless')

# driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()

driver.get(url1)

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
# time.sleep(1)

driver.refresh()

# time.sleep(5)

# driver.quit()