import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Get the users
tenant = User.objects.get(username='tenant1')
owner = User.objects.get(username='owner1')

client = Client()

# Login as owner
client.login(username='owner1', password='demo1234')

# Test POST API from owner to tenant
r_post = client.post('/chat/api/', {'partner_id': tenant.id, 'content': 'Hello from owner!'})
print("Owner POST status:", r_post.status_code)
print("Owner POST content:", r_post.content.decode('utf-8'))

# Login as tenant
client.logout()
client.login(username='tenant1', password='demo1234')

# Test GET API from tenant
r_get = client.get(f'/chat/api/?partner_id={owner.id}')
print("Tenant GET status:", r_get.status_code)
data = json.loads(r_get.content.decode('utf-8'))
print("Tenant GET messages count:", len(data.get('messages', [])))
if len(data.get('messages', [])) > 0:
    print("Last message:", data['messages'][-1]['content'])

# Test POST API from tenant to owner
r_post2 = client.post('/chat/api/', {'partner_id': owner.id, 'content': 'Hello back from tenant!'})
print("Tenant POST status:", r_post2.status_code)
print("Tenant POST content:", r_post2.content.decode('utf-8'))

