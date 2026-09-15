import re

view_code = '''
from django.shortcuts import get_object_or_404

@login_required
def user_edit(request, user_id):
    if not request.user.profile.is_owner():
        messages.error(request, 'Chỉ chủ trọ mới được sửa thông tin người dùng.')
        return redirect('dashboard')
        
    edit_user = get_object_or_404(User, id=user_id, profile__owner=request.user)
    profile = edit_user.profile
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        cccd = request.POST.get('cccd', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        errors = {}
        
        # Validate password if provided
        if password or password_confirm:
            if password != password_confirm:
                errors['password_confirm'] = 'Mật khẩu xác nhận không khớp!'
                
        # Validate Name
        name_regex = re.compile(r'^[a-zA-ZÀ-ỹ\s]+$')
        if not first_name or not name_regex.match(first_name):
            errors['first_name'] = 'Họ & Tên đệm chỉ được phép nhập chữ và không có ký tự đặc biệt'
        if not last_name or not name_regex.match(last_name):
            errors['last_name'] = 'Họ & Tên đệm chỉ được phép nhập chữ và không có ký tự đặc biệt'
            
        # Validate CCCD
        if not cccd or not re.match(r'^\d{12}$', cccd):
            errors['cccd'] = 'CCCD phải là đúng 12 số.'
        elif UserProfile.objects.filter(cccd=cccd).exclude(user=edit_user).exists():
            errors['cccd'] = 'Căn cước công dân đã tồn tại trên toàn hệ thống.'
            
        # Validate Phone
        if not phone or not re.match(r'^\d{10}$', phone):
            errors['phone'] = 'Số điện thoại phải là đúng 10 số.'
        elif UserProfile.objects.filter(phone=phone).exclude(user=edit_user).exists():
            errors['phone'] = 'Số điện thoại đã tồn tại trên toàn hệ thống.'
            
        # Validate Email
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = 'Email không hợp lệ.'
        elif User.objects.filter(email=email).exclude(id=edit_user.id).exists():
            errors['email'] = 'Email đã tồn tại trên toàn hệ thống.'
            
        if errors:
            post_data = {
                'username': edit_user.username,
                'first_name': first_name,
                'last_name': last_name,
                'cccd': cccd,
                'phone': phone,
                'email': email,
                'is_active': is_active,
            }
            return render(request, 'accounts/user_form.html', {'errors': errors, 'post_data': post_data, 'is_edit': True, 'user_id': user_id})
            
        try:
            with transaction.atomic():
                edit_user.first_name = first_name
                edit_user.last_name = last_name
                edit_user.email = email
                edit_user.is_active = is_active
                if password:
                    edit_user.set_password(password)
                edit_user.save()
                
                profile.phone = phone
                profile.cccd = cccd
                profile.save()
                
            messages.success(request, 'Cập nhật thông tin người dùng thành công!')
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            
    # GET method
    post_data = {
        'username': edit_user.username,
        'first_name': edit_user.first_name,
        'last_name': edit_user.last_name,
        'email': edit_user.email,
        'phone': profile.phone,
        'cccd': profile.cccd,
        'is_active': edit_user.is_active,
    }
    return render(request, 'accounts/user_form.html', {'post_data': post_data, 'is_edit': True, 'user_id': user_id})
'''

with open('accounts/views.py', 'a', encoding='utf-8') as f:
    f.write(view_code)
    
with open('accounts/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

urls_content = urls_content.replace("path('users/create/', views.user_create, name='user_create'),", "path('users/create/', views.user_create, name='user_create'),\n    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),")

with open('accounts/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

print('Updated accounts/views.py and urls.py')
