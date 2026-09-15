import re

content = '''

# ============================================================
# EPIC 5 — Models
# ============================================================

class Post(models.Model):
    """
    US13 - Bảng tin / Bài viết
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Chủ trọ')
    title = models.CharField(max_length=255, verbose_name='Tiêu đề')
    content = models.TextField(verbose_name='Nội dung')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'app_post'
        verbose_name = 'Bài viết'
        verbose_name_plural = 'Danh sách bài viết'
        ordering = ['-created_at']


class MaintenanceRequest(models.Model):
    """
    US12 - Yêu cầu sửa chữa / báo hỏng
    """
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('resolved', 'Đã xử lý'),
    ]
    
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests', verbose_name='Người thuê')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='maintenance_requests', verbose_name='Phòng')
    description = models.TextField(verbose_name='Mô tả chi tiết')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Yêu cầu {self.room.name} - {self.get_status_display()}"

    class Meta:
        db_table = 'app_maintenancerequest'
        verbose_name = 'Yêu cầu sửa chữa'
        verbose_name_plural = 'Yêu cầu sửa chữa'
        ordering = ['-created_at']


class Message(models.Model):
    """
    US14 - Chat nội bộ
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Người gửi')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='Người nhận')
    content = models.TextField(verbose_name='Nội dung')
    is_read = models.BooleanField(default=False, verbose_name='Đã đọc')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Từ {self.sender} đến {self.receiver}"

    class Meta:
        db_table = 'app_message'
        verbose_name = 'Tin nhắn'
        verbose_name_plural = 'Tin nhắn'
        ordering = ['created_at']
'''

with open('rooms/models.py', 'a', encoding='utf-8') as f:
    f.write(content)

print('Appended models to rooms/models.py')
