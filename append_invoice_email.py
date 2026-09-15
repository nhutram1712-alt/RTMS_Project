import re

content = '''
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

@login_required
@require_POST
def invoice_send_email(request, invoice_id):
    rooms = Room.objects.filter(owner=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, room__in=rooms)
    
    if invoice.status != 'chua_tt':
        messages.error(request, 'Chỉ có thể gửi nhắc nợ cho hóa đơn chưa thanh toán.')
        return redirect('invoice_list')
        
    try:
        tenant_assignment = invoice.room.tenant_assignment
        tenant = tenant_assignment.tenant
        
        if not tenant or not tenant.email:
            messages.error(request, 'Người thuê không có email hoặc phòng chưa có người thuê.')
            return redirect('invoice_list')
            
        # Gửi email
        subject = f'Nhắc thanh toán hóa đơn tháng {invoice.billing_month.strftime("%m/%Y")} - Phòng {invoice.room.name}'
        message = f'''Xin chào {tenant.get_full_name() or tenant.username},
        
Hóa đơn tháng {invoice.billing_month.strftime("%m/%Y")} cho Phòng {invoice.room.name} của bạn chưa được thanh toán.
Tổng số tiền: {invoice.total_amount:,.0f} VNĐ.

Vui lòng thanh toán qua số tài khoản: 123456789 (Ngân hàng VCB - Chủ tài khoản: Chủ trọ demo).
Mã tra cứu hóa đơn của bạn: HD{invoice.id:04d}.
Bạn có thể xem chi tiết tại hệ thống RTMS.

Trân trọng,
Quản lý dãy trọ.
'''
        # Ghi chú: Gửi bằng EMAIL_BACKEND console cho demo
        send_mail(
            subject,
            message,
            request.user.email or 'admin@rtms.local',
            [tenant.email],
            fail_silently=False,
        )
        
        messages.success(request, f'Đã gửi hóa đơn đến {tenant.email}!')
    except TenantAssignment.DoesNotExist:
        messages.error(request, 'Phòng này hiện không có người thuê.')
    except Exception as e:
        messages.error(request, f'Lỗi khi gửi email: {str(e)}')
        
    return redirect('invoice_list')
'''

with open('rooms/views.py', 'a', encoding='utf-8') as f:
    f.write(content)

with open('rooms/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

urls_content = urls_content.replace("path('invoices/', views.invoice_list, name='invoice_list'),", "path('invoices/', views.invoice_list, name='invoice_list'),\n    path('invoices/<int:invoice_id>/send_email/', views.invoice_send_email, name='invoice_send_email'),")

with open('rooms/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

print('Updated rooms/views.py and rooms/urls.py for invoice email')
