import urllib.request
import urllib.parse
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

# GET login page to get CSRF
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/login/')
    print("Login HTTP:", resp.status)
except Exception as e:
    print("Login Failed:", e)

csrf_token = ''
for cookie in cj:
    if cookie.name == 'csrftoken':
        csrf_token = cookie.value

# POST login
data = urllib.parse.urlencode({'username': 'owner1', 'password': 'demo1234', 'csrfmiddlewaretoken': csrf_token}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/login/', data=data)
try:
    resp = urllib.request.urlopen(req)
except Exception as e:
    pass

# Check /users/
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/users/')
    print("GET /users/ => HTTP", resp.status)
except Exception as e:
    print("GET /users/ Failed:", e)
    
# Check /users/create/
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/users/create/')
    print("GET /users/create/ => HTTP", resp.status)
except Exception as e:
    print("GET /users/create/ Failed:", e)

