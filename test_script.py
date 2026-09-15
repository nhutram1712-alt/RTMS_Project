import requests
from bs4 import BeautifulSoup

session = requests.Session()

# 1. Login as owner1
login_url = 'http://127.0.0.1:8000/login/'
r = session.get(login_url)
csrf_token = session.cookies.get('csrftoken')

r = session.post(login_url, data={
    'username': 'owner1',
    'password': 'password123',
    'csrfmiddlewaretoken': csrf_token
})
print("Login owner1 status:", r.status_code)
print("Dashboard URL after login:", r.url)

# 2. Go to /users/ to find a user to edit
r = session.get('http://127.0.0.1:8000/users/')
soup = BeautifulSoup(r.text, 'html.parser')
edit_link = soup.find('a', title='Sửa')
if edit_link:
    edit_url = edit_link['href']
    print(f"Found edit URL: {edit_url}")
    
    # Get edit form
    r = session.get(f"http://127.0.0.1:8000{edit_url}")
    csrf_token = session.cookies.get('csrftoken')
    soup_edit = BeautifulSoup(r.text, 'html.parser')
    username_input = soup_edit.find('input', {'name': 'username'})
    print(f"Edit form username field value: {username_input.get('value')}")
    
    # Submit edit form
    r = session.post(f"http://127.0.0.1:8000{edit_url}", data={
        'csrfmiddlewaretoken': csrf_token,
        'first_name': 'TestEdit',
        'last_name': 'Nguyen',
        'cccd': '012345678912',
        'phone': '0987654321',
        'email': 'edit@test.com',
        'is_active': 'on'
    })
    print(f"Edit submit status: {r.status_code}, redirect to: {r.url}")
else:
    print("No users found to edit.")

# 3. Create 'B Nguyễn Văn' user for testing tenant login
r = session.get('http://127.0.0.1:8000/users/create/')
csrf_token = session.cookies.get('csrftoken')
r = session.post('http://127.0.0.1:8000/users/create/', data={
    'csrfmiddlewaretoken': csrf_token,
    'username': 'bnguyenvan',
    'password': 'password123',
    'password_confirm': 'password123',
    'first_name': 'Văn',
    'last_name': 'B Nguyễn',
    'cccd': '111111111111',
    'phone': '0111111111',
    'email': 'bnguyenvan@test.com',
    'is_active': 'on'
})
print(f"Create user status: {r.status_code}, redirect to: {r.url}")

# 4. Logout owner1
r = session.get('http://127.0.0.1:8000/logout/')
print("Logout status:", r.status_code)

# 5. Login as bnguyenvan
r = session.get(login_url)
csrf_token = session.cookies.get('csrftoken')
r = session.post(login_url, data={
    'username': 'bnguyenvan',
    'password': 'password123',
    'csrfmiddlewaretoken': csrf_token
})
print("Login bnguyenvan status:", r.status_code)
print("URL after login:", r.url)

# 6. Check sidebar for bnguyenvan
r = session.get('http://127.0.0.1:8000/')
soup = BeautifulSoup(r.text, 'html.parser')
sidebar_links = [a.text.strip() for a in soup.select('.sidebar .nav-link')]
print("Tenant sidebar links:", sidebar_links)
