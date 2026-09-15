import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.contrib.auth.models import User

u = User.objects.get(username='bnguyenvan')
print("Role for bnguyenvan is:", u.profile.role)
print("Is owner method returns:", u.profile.is_owner())
