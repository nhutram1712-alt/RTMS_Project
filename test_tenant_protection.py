import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.test import Client

client = Client()

# Login as tenant
login_ok = client.login(username='bnguyenvan', password='demo1234')
print("Login bnguyenvan ok:", login_ok)

# 1. Check tenant dashboard
r = client.get('/tenant/dashboard/')
print("Tenant dashboard status:", r.status_code)
content = r.content.decode('utf-8')
print("Is 'Chưa được xếp phòng' in content?", 'Chưa được xếp phòng' in content)
print("Is 'Chưa có hóa đơn nào' in content?", 'Chưa có hóa đơn nào' in content)

# 2. Try to access owner dashboard
r_owner = client.get('/')
print("Owner dashboard (/) status:", r_owner.status_code)
if r_owner.status_code in [301, 302]:
    print("Redirect to:", r_owner.url)

# 3. Try to access another owner URL (e.g. room_create)
r_create = client.get('/rooms/create/')
print("Room create status:", r_create.status_code)
if r_create.status_code in [301, 302]:
    print("Redirect to:", r_create.url)

# 4. Check if tenant dashboard has 'Thông tin phòng đang thuê'
print("Is 'Thông tin phòng đang thuê' in tenant content?", 'Thông tin phòng đang thuê' in content)
