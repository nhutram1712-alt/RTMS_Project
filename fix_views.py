import re

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, clean up the wrong injections
wrong_injection = '''
    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')
'''

# The previous script actually wrote the unicode as it was, but let's just use regex to remove it
# Since the previous script ran in cp1252 it might have mangled the characters if not careful, wait no, I used encoding='utf-8' in python script!
content = content.replace(wrong_injection, "")

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Cleaned up")

