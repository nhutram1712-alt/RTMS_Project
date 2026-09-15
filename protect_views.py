import sys
import re

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

owner_views = [
    'room_create', 'room_edit', 'room_delete', 'room_status_update',
    'invoice_create', 'calculate_invoice_preview', 'invoice_list', 'invoice_send_email'
]

auth_check = '''
    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')
'''

for view_name in owner_views:
    # Find the function definition
    pattern = r'(def ' + view_name + r'\(.*?\):(?:.*?""")?)'
    
    # We want to insert the auth_check right after the def or docstring.
    # The regex matches the function def and optionally the docstring.
    match = re.search(pattern, content, re.DOTALL)
    if match:
        original = match.group(1)
        # Check if already protected
        if "is_owner" not in content[match.end():match.end()+200]:
            replacement = original + "\n" + auth_check
            content = content.replace(original, replacement)
            print(f"Protected {view_name}")

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated rooms/views.py")
