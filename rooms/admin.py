from django.contrib import admin
from .models import Room, TenantAssignment, Invoice

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor', 'status', 'base_rent', 'owner']
    list_filter = ['status', 'floor']
    search_fields = ['name']

@admin.register(TenantAssignment)
class TenantAssignmentAdmin(admin.ModelAdmin):
    list_display = ['room', 'tenant', 'move_in_date', 'lease_duration', 'deposit']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['room', 'billing_month', 'total_amount', 'status']
    list_filter = ['status', 'billing_month']
