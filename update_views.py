import sys

with open('rooms/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add tenant_dashboard
tenant_dashboard_code = '''
@login_required
def tenant_dashboard(request):
    """
    US07/US16: Trang chủ dành riêng cho Người thuê.
    Hiển thị thông tin phòng đang thuê và lịch sử hóa đơn cá nhân.
    """
    if request.user.profile.is_owner():
        return redirect('dashboard')
        
    assignment = TenantAssignment.objects.filter(tenant=request.user).select_related('room').first()
    invoices = []
    if assignment:
        invoices = Invoice.objects.filter(room=assignment.room).order_by('-created_at')
        
    context = {
        'assignment': assignment,
        'invoices': invoices,
    }
    return render(request, 'rooms/tenant_dashboard.html', context)
'''

# We also need to add check for is_owner in dashboard
dashboard_code = '''
@login_required
def dashboard(request):
    """
    Trang tổng quan — hiển thị danh sách phòng của chủ trọ
    """
    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        return redirect('tenant_dashboard')
        
    rooms = Room.objects.filter(owner=request.user).order_by('name')
'''

content = content.replace('''
@login_required
def dashboard(request):
    """
    Trang tổng quan — hiển thị danh sách phòng của chủ trọ
    """
    rooms = Room.objects.filter(owner=request.user).order_by('name')'''.strip(), dashboard_code.strip())

# append tenant_dashboard to the top area or bottom
content = content.replace("def dashboard(request):", tenant_dashboard_code.strip() + "\n\n" + "@login_required\ndef dashboard(request):")

with open('rooms/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated views.py dashboard")
