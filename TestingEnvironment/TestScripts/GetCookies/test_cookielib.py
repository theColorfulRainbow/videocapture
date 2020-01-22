import urllib, urllib2, cookielib
import requests

EMAIL = 's1628465@ed.ac.uk'
PASSWORD = 'anj3la.1.yoga'
URL = 'https://echo360.org.uk/directLogin'

values = {'username': EMAIL,
          'password': PASSWORD}

session = requests.Session()
print(session.cookies.get_dict())
# r = requests.post(URL, data=values)
r = session.get(URL, auth=(EMAIL, PASSWORD))
print(r.content)
print(r.status_code)
print(session.cookies.get_dict())
# print r.content
