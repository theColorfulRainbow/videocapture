'''
Scripts tahat takes cookies from echo360 & stores tehm in curent dir
'''

import time
import pickle
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

url = 'https://echo360.org.uk/directLogin'
email = 's1628465@ed.ac.uk'
password = 'anj3la.1.yoga'

options = Options()
# not graphical display 
options.add_argument('--headless') 			

# start new session
driver = webdriver.Firefox(options=options)
# driver = webdriver.Firefox()

# navigate to url
driver.get(url)

# add your email & password
driver.find_element_by_name('email').send_keys(email)
driver.find_element_by_name('password').send_keys(password)

# clock on login button
driver.find_element_by_name('action').click()

# get cokies once you logged in
pickle.dump(driver.get_cookies(),open("cookies.pkl","wb"))

# dump cookies into a .pkl file (format doesn't matter)
cookies = pickle.load(open("cookies.pkl", "rb"))
# write cookies to a .txt file in utf-8 format
cookies_txt = open('cookies.txt','w')
for cookie in cookies:
    cookies_txt.write(str(cookie)+'\n')
cookies_txt.close()

# print current page content
# print(driver.page_source.encode('utf-8'))

time.sleep(1)

# exit driver session
driver.quit()