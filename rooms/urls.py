"""
URL patterns cho app rooms
"""
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('tenant/dashboard/', views.tenant_dashboard, name='tenant_dashboard'),

    # US01 — CRUD phòng
    path('rooms/create/', views.room_create, name='room_create'),
    path('rooms/<int:room_id>/edit/', views.room_edit, name='room_edit'),
    path('rooms/<int:room_id>/delete/', views.room_delete, name='room_delete'),

    # US02 — Cập nhật trạng thái
    path('rooms/<int:room_id>/status/', views.room_status_update, name='room_status_update'),

    # US03/04/05 — Hóa đơn
    path('rooms/<int:room_id>/invoice/', views.invoice_create, name='invoice_create'),
    path('rooms/<int:room_id>/invoice/preview/', views.calculate_invoice_preview, name='invoice_preview'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:invoice_id>/send_email/', views.invoice_send_email, name='invoice_send_email'),
    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:req_id>/resolve/', views.maintenance_resolve, name='maintenance_resolve'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('chat/', views.chat_view, name='chat_view'),
    path('chat/api/', views.chat_api, name='chat_api'),

    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
]
