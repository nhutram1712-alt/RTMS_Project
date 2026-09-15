import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

owner = User.objects.get(username='owner1')
tenant = User.objects.get(username='tenant1')

client = Client()
client.login(username='tenant1', password='demo1234')

# Test GET API from tenant
r_get = client.get(f'/chat/api/?partner_id={owner.id}')
print("Tenant GET status:", r_get.status_code)
if r_get.status_code == 200:
    print("Content:", r_get.content.decode('utf-8'))

