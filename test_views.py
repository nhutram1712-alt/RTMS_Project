import urllib.request
import urllib.parse
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# GET /login/
r = opener.open('http://127.0.0.1:8000/login/')
csrftoken = ''
for cookie in cj:
    if cookie.name == 'csrftoken':
        csrftoken = cookie.value
        break

# POST /login/
data = urllib.parse.urlencode({
    'username': 'owner1',
    'password': 'demo1234',
    'csrfmiddlewaretoken': csrftoken
}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/login/', data=data)
req.add_header('Referer', 'http://127.0.0.1:8000/login/')
try:
    r2 = opener.open(req)
    print('Login HTTP:', r2.status)
except Exception as e:
    print('Login Failed:', e)

# GET /rooms/create/
try:
    r3 = opener.open('http://127.0.0.1:8000/rooms/create/')
    print('GET /rooms/create/ => HTTP', r3.status)
except Exception as e:
    print('GET /rooms/create/ Failed:', e)

# GET /
try:
    r4 = opener.open('http://127.0.0.1:8000/')
    print('GET / => HTTP', r4.status)
except Exception as e:
    print('GET / Failed:', e)
