import sys

with open('accounts/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("redirect('dashboard')", "redirect('tenant_dashboard')")

with open('accounts/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated accounts/views.py")
