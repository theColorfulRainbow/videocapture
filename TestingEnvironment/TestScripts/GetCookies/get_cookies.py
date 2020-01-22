'''
Scripts tahat takes cookies from echo360 & stores tehm in curent dir
Script made as a method that can be called
'''

import time
import pickle
import requests
import http.cookiejar as cookielib
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

URL = 'https://echo360.org.uk/directLogin'
EMAIL = 's1628465@ed.ac.uk'
PASSWORD = 'anj3la.1.yoga'

def parseCookieFile(cookies):
    cookies = {}
    for cookie in cookies:
        if not re.match(r'^\#', line):
            lineFields = line.strip().split('\t')
            cookies[lineFields[5]] = cookie[6]
    return cookies

def get_cookies(url=URL,email=None,password=None):
    if(email==None):
        email = EMAIL
        print('email = {}'.format(EMAIL))
    if(password==None):
        password = PASSWORD
    	print('password = {}'.format(PASSWORD))
    options = Options()
    # not graphical display
    options.add_argument('--headless')

    # start new session
    # driver = webdriver.Firefox(options=options)
    driver = webdriver.Firefox()
    try:
    	#raw_input()
    	# navigate to url
    	driver.get(url)
    	#raw_input()
    	# add your email & password
    	driver.find_element_by_name('email').send_keys(email)
    	#raw_input()
    	driver.find_element_by_name('password').send_keys(password)
    	#raw_input()
    	# clock on login button
    	driver.find_element_by_name('action').click()

    	time.sleep(1)

    	cookie_list = driver.get_cookies()
    	cookie_dict = {}
        cookies_txt = open('cookies.txt','w')
        for cookie in cookie_list:
            cookie_txt = ''
            for key in cookie:
                print(key)
                cookie_txt += str(cookie[key])+'\t'
            cookie_txt += '\n'
            cookies_txt.write(str(cookie_txt))
            # print(cookie_txt)
    		# print cookie
        cookies_txt.close()
    	# print('\n\n{}'.format(cookie_list))

    	raw_input()

    	# get cokies once you logged in
    	pickle.dump(driver.get_cookies(),open("cookies.pkl","wb"))

    	# dump cookies into a .pkl file (format doesn't matter)
    	cookies = pickle.load(open("cookies.pkl", "rb"))
    	# write cookies to a .txt file in utf-8 format
    	cookies_txt = open('cookies.txt','w')
    	for cookie in cookies:
    	    cookies_txt.write(str(cookie)+'\n')
    	cookies_txt.close()

    	time.sleep(1)
    except Exception as ex:
        print(ex)
    	# exit driver session
    	driver.quit()

def main():
	get_cookies()

if __name__ == '__main__':
	main()
