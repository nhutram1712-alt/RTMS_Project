"""
Models cho app accounts
Mở rộng User Django với UserProfile
"""
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Mở rộng thông tin User mặc định của Django
    """
    ROLE_CHOICES = [
        ('owner', 'Chủ trọ'),
        ('tenant', 'Người thuê'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenants', null=True, blank=True, verbose_name='Chủ trọ')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant', verbose_name='Vai trò')
    phone = models.CharField(max_length=10, blank=True, verbose_name='Số điện thoại')
    cccd = models.CharField(max_length=12, blank=True, verbose_name='Căn cước công dân')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def is_owner(self):
        return self.role == 'owner'

    def is_tenant(self):
        return self.role == 'tenant'

    class Meta:
        verbose_name = 'Hồ sơ người dùng'
        verbose_name_plural = 'Hồ sơ người dùng'
