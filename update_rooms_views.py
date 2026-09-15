import re

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace tenants query in room_create and room_edit
content = content.replace("tenants = User.objects.filter(profile__role='tenant')", "tenants = User.objects.filter(profile__role='tenant', profile__owner=request.user)")

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated rooms/views.py for tenants filter')
