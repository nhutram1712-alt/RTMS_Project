import re

content = '''
import re
from django.db import transaction
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def user_list(request):
    if not request.user.profile.is_owner():
        messages.error(request, 'Chỉ chủ trọ mới được xem danh sách người dùng.')
        return redirect('dashboard')
    
    # Lấy danh sách tenant thuộc owner hiện tại
    tenants = UserProfile.objects.filter(owner=request.user, role='tenant').select_related('user')
    return render(request, 'accounts/user_list.html', {'users': tenants})


@login_required
def user_create(request):
    if not request.user.profile.is_owner():
        messages.error(request, 'Chỉ chủ trọ mới được tạo người dùng.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        first_name = request.POST.get('first_name', '').strip()  # Tên
        last_name = request.POST.get('last_name', '').strip()    # Họ & Tên đệm
        cccd = request.POST.get('cccd', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        
        errors = {}
        # Validate username
        if not username:
            errors['username'] = 'Vui lòng nhập tên đăng nhập.'
        elif User.objects.filter(username=username).exists():
            errors['username'] = 'Tên đăng nhập đã tồn tại.'
            
        # Validate password
        if not password:
            errors['password'] = 'Vui lòng nhập mật khẩu.'
        if password != password_confirm:
            errors['password_confirm'] = 'Mật khẩu xác nhận không khớp!'
            
        # Validate Name (chữ, không ký tự đặc biệt/số)
        name_regex = re.compile(r'^[a-zA-ZÀ-ỹ\s]+$')
        if not first_name or not name_regex.match(first_name):
            errors['first_name'] = 'Họ & Tên đệm chỉ được phép nhập chữ và không có ký tự đặc biệt'
        if not last_name or not name_regex.match(last_name):
            errors['last_name'] = 'Họ & Tên đệm chỉ được phép nhập chữ và không có ký tự đặc biệt'
            
        # Validate CCCD
        if not cccd or not re.match(r'^\d{12}$', cccd):
            errors['cccd'] = 'CCCD phải là đúng 12 số.'
        elif UserProfile.objects.filter(cccd=cccd).exists():
            errors['cccd'] = 'Căn cước công dân đã tồn tại trên toàn hệ thống.'
            
        # Validate Phone
        if not phone or not re.match(r'^\d{10}$', phone):
            errors['phone'] = 'Số điện thoại phải là đúng 10 số.'
        elif UserProfile.objects.filter(phone=phone).exists():
            errors['phone'] = 'Số điện thoại đã tồn tại trên toàn hệ thống.'
            
        # Validate Email
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = 'Email không hợp lệ.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email đã tồn tại trên toàn hệ thống.'
            
        if errors:
            post_data = {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'cccd': cccd,
                'phone': phone,
                'email': email,
                'is_active': is_active,
            }
            return render(request, 'accounts/user_form.html', {'errors': errors, 'post_data': post_data})
            
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    is_active=is_active
                )
                UserProfile.objects.create(
                    user=user,
                    owner=request.user,
                    role='tenant',
                    phone=phone,
                    cccd=cccd
                )
            messages.success(request, 'Tạo tài khoản người thuê thành công!')
            return redirect('user_list')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra: {str(e)}')
            
    return render(request, 'accounts/user_form.html')
'''

with open('accounts/views.py', 'a', encoding='utf-8') as f:
    f.write(content)

print('Updated accounts/views.py')
