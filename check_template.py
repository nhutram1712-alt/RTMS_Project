import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.test import Client

client = Client()
client.login(username='bnguyenvan', password='demo1234')

r = client.get('/')
content = r.content.decode('utf-8')

import re
matches = re.findall(r'<li class="nav-item">.*?</li>', content, re.DOTALL)
print("Nav items rendered:")
for m in matches:
    if 'Thêm phòng' in m:
        print("FOUND THEM PHONG:", m.strip())
        break
else:
    print("No Them phong found in nav items.")
