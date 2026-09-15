import sys

content = """
from django.http import JsonResponse
from django.db.models import Q

# ============================================================
# EPIC 5 — Maintenance Requests (Báo hỏng)
# ============================================================

@login_required
def maintenance_list(request):
    if request.user.profile.is_tenant():
        if request.method == 'POST':
            description = request.POST.get('description', '').strip()
            if not description:
                messages.error(request, 'Vui lòng nhập mô tả báo hỏng.')
            else:
                assignment = request.user.tenant_assignments.first()
                if assignment:
                    MaintenanceRequest.objects.create(
                        tenant=request.user,
                        room=assignment.room,
                        description=description,
                    )
                    messages.success(request, 'Đã gửi yêu cầu báo hỏng.')
                else:
                    messages.error(request, 'Bạn chưa được gán vào phòng nào.')
            return redirect('maintenance_list')
            
        requests = MaintenanceRequest.objects.filter(tenant=request.user)
        return render(request, 'rooms/maintenance_tenant.html', {'requests': requests})
    else:
        rooms = Room.objects.filter(owner=request.user)
        requests = MaintenanceRequest.objects.filter(room__in=rooms)
        pending_requests = requests.filter(status='pending')
        resolved_requests = requests.filter(status='resolved')
        return render(request, 'rooms/maintenance_owner.html', {
            'pending_requests': pending_requests,
            'resolved_requests': resolved_requests,
        })


@login_required
@require_POST
def maintenance_resolve(request, req_id):
    if not request.user.profile.is_owner():
        return redirect('dashboard')
        
    rooms = Room.objects.filter(owner=request.user)
    m_req = get_object_or_404(MaintenanceRequest, id=req_id, room__in=rooms)
    m_req.status = 'resolved'
    m_req.save()
    messages.success(request, 'Đã cập nhật trạng thái xử lý.')
    return redirect('maintenance_list')


# ============================================================
# EPIC 5 — Posts (Bảng tin)
# ============================================================

@login_required
def post_list(request):
    if request.user.profile.is_tenant():
        owner = request.user.profile.owner
        posts = Post.objects.filter(owner=owner) if owner else []
        return render(request, 'rooms/post_tenant.html', {'posts': posts})
    else:
        if request.method == 'POST':
            title = request.POST.get('title', '').strip()
            content = request.POST.get('content', '').strip()
            
            if not title or not content:
                messages.error(request, 'Vui lòng điền đủ Tiêu đề và Nội dung.')
            else:
                Post.objects.create(owner=request.user, title=title, content=content)
                messages.success(request, 'Đã đăng bài viết/thông báo mới thành công!')
            return redirect('post_list')
            
        posts = Post.objects.filter(owner=request.user)
        return render(request, 'rooms/post_owner.html', {'posts': posts})


@login_required
def post_edit(request, post_id):
    if not request.user.profile.is_owner():
        return redirect('dashboard')
        
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        
        if not title or not content:
            messages.error(request, 'Vui lòng điền đủ Tiêu đề và Nội dung.')
        else:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Đã cập nhật bài viết/thông báo thành công!')
            return redirect('post_list')
            
    return render(request, 'rooms/post_edit.html', {'post': post})


@login_required
@require_POST
def post_delete(request, post_id):
    if not request.user.profile.is_owner():
        return redirect('dashboard')
        
    post = get_object_or_404(Post, id=post_id, owner=request.user)
    post.delete()
    messages.success(request, 'Đã xóa bài viết thành công!')
    return redirect('post_list')


# ============================================================
# EPIC 5 — Chat (Tin nhắn)
# ============================================================

@login_required
def chat_view(request):
    if request.user.profile.is_tenant():
        owner = request.user.profile.owner
        assignment = request.user.tenant_assignments.first()
        if not assignment or assignment.room.status != 'dang_thue':
            messages.error(request, 'Bạn chỉ có thể chat khi đang thuê phòng.')
            return redirect('dashboard')
        return render(request, 'rooms/chat.html', {'chat_partner': owner, 'is_owner': False})
    else:
        active_rooms = Room.objects.filter(owner=request.user, status='dang_thue')
        selected_tenant_id = request.GET.get('tenant_id')
        selected_tenant = None
        if selected_tenant_id:
            try:
                selected_tenant = User.objects.get(id=selected_tenant_id, profile__role='tenant', profile__owner=request.user)
            except User.DoesNotExist:
                pass
                
        return render(request, 'rooms/chat.html', {
            'is_owner': True,
            'active_rooms': active_rooms,
            'selected_tenant': selected_tenant
        })

@login_required
def chat_api(request):
    partner_id = request.GET.get('partner_id') or request.POST.get('partner_id')
    if not partner_id:
        return JsonResponse({'error': 'Missing partner_id'}, status=400)
        
    try:
        partner = User.objects.get(id=partner_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
        
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(sender=request.user, receiver=partner, content=content)
            return JsonResponse({'status': 'ok'})
        return JsonResponse({'error': 'Empty message'}, status=400)
        
    messages_qs = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=partner)) | 
        (Q(sender=partner) & Q(receiver=request.user))
    )
    
    Message.objects.filter(sender=partner, receiver=request.user, is_read=False).update(is_read=True)
    
    data = []
    for msg in messages_qs:
        data.append({
            'id': msg.id,
            'sender_id': msg.sender_id,
            'content': msg.content,
            'created_at': msg.created_at.strftime('%H:%M %d/%m/%Y'),
        })
        
    return JsonResponse({'messages': data})

"""

with open('rooms/views.py', 'a', encoding='utf-8') as f:
    f.write(content)

urls_content_append = """
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:req_id>/resolve/', views.maintenance_resolve, name='maintenance_resolve'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('chat/', views.chat_view, name='chat_view'),
    path('chat/api/', views.chat_api, name='chat_api'),
"""

with open('rooms/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

urls_content = urls_content.replace("path('invoices/<int:invoice_id>/send_email/', views.invoice_send_email, name='invoice_send_email'),", "path('invoices/<int:invoice_id>/send_email/', views.invoice_send_email, name='invoice_send_email')," + urls_content_append)

with open('rooms/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_content)

print('Updated rooms/views.py and rooms/urls.py for epic 5')
