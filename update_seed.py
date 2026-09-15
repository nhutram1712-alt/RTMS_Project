import re

with open('seed_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Append owner to tenant1's profile creation
content = content.replace("profile = UserProfile.objects.create(user=tenant, role='tenant')", "profile = UserProfile.objects.create(user=tenant, role='tenant', owner=owner)")
content = content.replace("profile = UserProfile.objects.create(user=tenant2, role='tenant')", "profile = UserProfile.objects.create(user=tenant2, role='tenant', owner=owner)")

with open('seed_data.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated seed_data.py')
