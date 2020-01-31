import requests
import scrapy
from scrapy.http import FormRequest
from bs4 import BeautifulSoup

with requests.Session() as my_session:
    EMAIL = 's1628465@ed.ac.uk'
    PASSWORD = 'anj3la.1.yoga'
    URL = 'https://echo360.org.uk/directLogin'

    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }

    login_data = {
        'nstitutionId': '',
        'userId': '',
        'afterLoginUrl': '',
        'email': 's1628465@ed.ac.uk',
        'password': 'anj3la.1.yoga',
        'captchaBypassKey': '',
        'action': 'Save'
    }

    my_response = my_session.get(URL,headers=headers)
    
    bs_content = BeautifulSoup(my_response.content,'lxml')
    
    action = bs_content.find('form')['action']
    str_remove = '/login?csrfToken='
    csrfToken  = action.replace(str_remove,'')
    
    print(csrfToken)
    # print('not removed: {}'.format(action))
    # print('removed: {}'.format(action.replace(str_remove,'')))
    # token = bs_content.find("input", {"name":"csrf_token"})["value"]
    # print('my_token={}'.format(token))
    
    # need to find & pass 'id' i think
    # print(my_soup.find('dvi'))
    
    # login_data['id'] = my_soup.find('input',attr={'name':'id'})['value']


    # my_response = my_session.post(URL,data=login_data, headers=headers)
    # print(my_response.content)
    # my_cookies = my_response.cookies.get_dict()
    # print(my_cookies) 
    
    # csrftoken = my_session.cookies['csrftoken']
    # login_data = dict(email = EMAIL, password = PASSWORD)

