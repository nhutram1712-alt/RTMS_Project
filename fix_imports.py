import re

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = "from django.db.models import Q\n" + content

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed imports")

