import os
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

client.login(username='owner1', password='demo1234')
print("Logged in as owner1")

r = client.get('/users/')
print("Users page status:", r.status_code)
content = r.content.decode('utf-8')

# Find edit URL e.g., href="/users/2/edit/"
match = re.search(r'href="(/users/\d+/edit/)"', content)
if match:
    edit_url = match.group(1)
    print(f"Found edit URL: {edit_url}")
    
    r = client.get(edit_url)
    print("Edit form GET status:", r.status_code)
    
    r = client.post(edit_url, data={
        'first_name': 'TestEdit',
        'last_name': 'Nguyen',
        'cccd': '012345678912',
        'phone': '0987654321',
        'email': 'edit@test.com',
        'is_active': 'on'
    })
    print(f"Edit submit status: {r.status_code}, redirect to: {r.url if hasattr(r, 'url') else r.headers.get('Location')}")
else:
    print("No users found to edit.")

r = client.post('/users/create/', data={
    'username': 'bnguyenvan',
    'password': 'demo1234',
    'password_confirm': 'demo1234',
    'first_name': 'Văn',
    'last_name': 'B Nguyễn',
    'cccd': '111111111111',
    'phone': '0111111111',
    'email': 'bnguyenvan@test.com',
    'is_active': 'on'
})
print(f"Create user status: {r.status_code}, redirect to: {r.url if hasattr(r, 'url') else r.headers.get('Location')}")

client.logout()
print("Logged out owner1")

login_ok = client.login(username='bnguyenvan', password='demo1234')
print("Login bnguyenvan ok:", login_ok)

r = client.get('/')
print("Tenant dashboard status:", r.status_code)
content = r.content.decode('utf-8')

# simple check for sidebar links
print("Is 'Trang chu' in tenant HTML?", 'Trang ch' in content)
print("Is 'Bang tin' in tenant HTML?", 'B' in content)
print("Is 'Them phong' in tenant HTML?", 'Th' in content and 'ph' in content)
print("Are owner links hidden?", 'Thêm phòng' not in content)
