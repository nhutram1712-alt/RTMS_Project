import urllib.request
import urllib.parse
from http.cookiejar import CookieJar

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

# GET login page to get CSRF
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000/login/')
except Exception as e:
    pass

csrf_token = ''
for cookie in cj:
    if cookie.name == 'csrftoken':
        csrf_token = cookie.value

# POST login as owner1
data = urllib.parse.urlencode({'username': 'owner1', 'password': 'demo1234', 'csrfmiddlewaretoken': csrf_token}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/login/', data=data)
try:
    resp = urllib.request.urlopen(req)
except Exception as e:
    pass

endpoints = ['http://127.0.0.1:8000/dashboard/', 'http://127.0.0.1:8000/rooms/posts/', 'http://127.0.0.1:8000/rooms/maintenance/']

for url in endpoints:
    try:
        resp = urllib.request.urlopen(url)
        print(f"GET {url} => {resp.status}")
        html = resp.read().decode('utf-8')
        if '101' in html and '102' in html and url == 'http://127.0.0.1:8000/dashboard/':
            print("Dashboard has rooms!")
    except Exception as e:
        print(f"GET {url} Failed: {e}")

