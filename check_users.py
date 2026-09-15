import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.contrib.auth.models import User

owners = User.objects.filter(profile__role='owner')
print("Owners:")
for o in owners:
    print(o.username, o.check_password('password123'))

tenants = User.objects.filter(profile__role='tenant')
print("Tenants:")
for t in tenants:
    print(t.username)
