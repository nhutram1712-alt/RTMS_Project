"""
Models cho app rooms — Room, TenantAssignment, Invoice
Dựa theo ERD và Acceptance Criteria trong SRS
"""
import json
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.core.exceptions import ValidationError


# ===== DANH SÁCH TIỆN NGHI =====
AMENITY_CHOICES = [
    ('dieu_hoa', 'Điều hòa'),
    ('may_nuoc_nong', 'Máy nước nóng'),
    ('tu_lanh', 'Tủ lạnh'),
    ('ban_cong', 'Ban công'),
    ('may_giat', 'Máy giặt'),
    ('wifi', 'Wifi'),
    ('noi_that', 'Nội thất cơ bản'),
    ('cho_de_xe', 'Chỗ để xe'),
    ('bep', 'Bếp'),
    ('camera', 'Camera an ninh'),
]

# ===== TRẠNG THÁI PHÒNG =====
ROOM_STATUS_CHOICES = [
    ('trong', 'Trống'),
    ('dang_thue', 'Đang thuê'),
    ('da_coc', 'Đã cọc'),
    ('sua_chua', 'Sửa chữa'),
]

# ===== TRẠNG THÁI HÓA ĐƠN =====
INVOICE_STATUS_CHOICES = [
    ('nhap', 'Nháp'),
    ('chua_tt', 'Chưa thanh toán'),
]


class Room(models.Model):
    """
    Model phòng trọ theo SRS
    Bao gồm thông tin cơ bản, đơn giá, chỉ số điện/nước
    """
    # Thông tin cơ bản
    name = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Tên phòng',
        validators=[RegexValidator(r'^\d+$', 'Tên phòng chỉ được chứa số')]
    )
    floor = models.IntegerField(
        verbose_name='Tầng',
        validators=[MinValueValidator(0)]
    )
    area = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Diện tích (m²)'
    )
    max_occupancy = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Số người tối đa'
    )
    # Tiện nghi lưu dạng JSON list
    amenities = models.TextField(
        blank=True, default='[]',
        verbose_name='Tiện nghi'
    )

    # Đơn giá dịch vụ
    base_rent = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Giá thuê (đ/tháng)'
    )
    electricity_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Đơn giá điện (đ/kWh)'
    )
    water_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Đơn giá nước (đ/m³)'
    )
    trash_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Phí rác (đ/tháng)'
    )
    internet_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Phí internet (đ/tháng)'
    )

    # Chỉ số đầu kỳ (cập nhật sau mỗi lần tạo hóa đơn)
    current_electricity = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True, default=0,
        verbose_name='Chỉ số điện hiện tại (kWh)'
    )
    current_water = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True, default=0,
        verbose_name='Chỉ số nước hiện tại (khối)'
    )

    # Trạng thái phòng
    status = models.CharField(
        max_length=20,
        choices=ROOM_STATUS_CHOICES,
        default='trong',
        verbose_name='Trạng thái'
    )

    # Chủ sở hữu
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='rooms',
        verbose_name='Chủ trọ'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_amenities_list(self):
        """Trả về list tiện nghi từ JSON string"""
        try:
            return json.loads(self.amenities)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_amenities_list(self, amenity_list):
        """Lưu list tiện nghi thành JSON string"""
        self.amenities = json.dumps(amenity_list)

    def get_amenities_display_list(self):
        """Trả về list tên tiện nghi hiển thị"""
        amenity_dict = dict(AMENITY_CHOICES)
        return [amenity_dict.get(a, a) for a in self.get_amenities_list()]

    def get_status_display_class(self):
        """Bootstrap badge class tương ứng với trạng thái"""
        mapping = {
            'trong': 'success',
            'dang_thue': 'primary',
            'da_coc': 'warning',
            'sua_chua': 'danger',
        }
        return mapping.get(self.status, 'secondary')

    def can_delete(self):
        """
        Chỉ được xóa nếu phòng không đang thuê hoặc đã cọc (BR-01)
        """
        return self.status not in ('dang_thue', 'da_coc')

    def needs_tenant_info(self):
        """Phòng cần thông tin người thuê nếu trạng thái là đang thuê hoặc đã cọc"""
        return self.status in ('dang_thue', 'da_coc')

    def __str__(self):
        return f"Phòng {self.name}"

    class Meta:
        verbose_name = 'Phòng trọ'
        verbose_name_plural = 'Danh sách phòng'
        ordering = ['name']


class TenantAssignment(models.Model):
    """
    Thông tin người thuê gắn với phòng
    Enable khi status = "Đang thuê" hoặc "Đã cọc"
    """
    room = models.OneToOneField(
        Room, on_delete=models.CASCADE,
        related_name='tenant_assignment',
        verbose_name='Phòng'
    )
    tenant = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='tenant_assignments',
        verbose_name='Người thuê'
    )
    move_in_date = models.DateField(verbose_name='Ngày nhận phòng')
    lease_duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Thời hạn thuê (tháng)'
    )
    deposit = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(1)],
        verbose_name='Tiền cọc (đ)'
    )
    contract_image = models.ImageField(
        upload_to='contracts/',
        null=True, blank=True,
        verbose_name='Ảnh hợp đồng'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def expiration_date(self):
        if self.move_in_date and self.lease_duration:
            import calendar
            month = self.move_in_date.month - 1 + self.lease_duration
            year = self.move_in_date.year + month // 12
            month = month % 12 + 1
            day = min(self.move_in_date.day, calendar.monthrange(year, month)[1])
            from datetime import date
            return date(year, month, day)
        return None

    def days_until_expiration(self):
        from datetime import date
        exp = self.expiration_date()
        if exp:
            return (exp - date.today()).days
        return None

    def __str__(self):
        tenant_name = self.tenant.get_full_name() if self.tenant else 'Không rõ'
        return f"{self.room} — {tenant_name}"

    class Meta:
        verbose_name = 'Thông tin người thuê'
        verbose_name_plural = 'Thông tin người thuê'


class Invoice(models.Model):
    """
    Hóa đơn hàng tháng — tối thiểu cho Epic 2
    Unique per room per billing_month (BR-02)
    """
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='Phòng'
    )
    # billing_month lưu ngày đầu tháng, ví dụ: 2026-09-01
    billing_month = models.DateField(verbose_name='Kỳ thanh toán (tháng)')

    # Chỉ số điện nước
    old_electricity = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Chỉ số điện cũ (kWh)'
    )
    new_electricity = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Chỉ số điện mới (kWh)'
    )
    old_water = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Chỉ số nước cũ (khối)'
    )
    new_water = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Chỉ số nước mới (khối)'
    )

    # Snapshot giá tại thời điểm tạo hóa đơn (không thay đổi khi room update)
    base_rent = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Tiền phòng')
    electricity_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Đơn giá điện')
    water_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Đơn giá nước')
    trash_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Phí rác')
    internet_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Phí internet')

    # Phụ phí
    extra_fee = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0,
        verbose_name='Phụ phí'
    )
    extra_fee_reason = models.TextField(blank=True, verbose_name='Lý do phụ phí')

    # Tổng tiền (làm tròn đến đồng, readonly)
    total_amount = models.DecimalField(
        max_digits=14, decimal_places=0,
        verbose_name='Tổng cộng thanh toán (đ)'
    )

    status = models.CharField(
        max_length=10,
        choices=INVOICE_STATUS_CHOICES,
        default='nhap',
        verbose_name='Trạng thái'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        """
        Tính tổng tiền theo công thức từ SRS US05:
        Tổng = Tiền phòng + Tiền điện + Tiền nước + Rác + Internet + Phụ phí
        """
        # Tiền điện = (chỉ số mới - chỉ số cũ) × đơn giá
        electricity_cost = (self.new_electricity - self.old_electricity) * self.electricity_price
        # Tiền nước = (chỉ số mới - chỉ số cũ) × đơn giá
        water_cost = (self.new_water - self.old_water) * self.water_price
        # Dịch vụ = rác + internet
        service_cost = self.trash_price + self.internet_price
        # Phụ phí mặc định là 0
        extra = self.extra_fee or 0
        # Tổng cộng
        total = self.base_rent + electricity_cost + water_cost + service_cost + extra
        return round(total, 0)

    def get_electricity_cost(self):
        return (self.new_electricity - self.old_electricity) * self.electricity_price

    def get_water_cost(self):
        return (self.new_water - self.old_water) * self.water_price

    def get_service_cost(self):
        return self.trash_price + self.internet_price

    def __str__(self):
        return f"HD - {self.room} - {self.billing_month.strftime('%m/%Y')}"

    class Meta:
        verbose_name = 'Hóa đơn'
        verbose_name_plural = 'Danh sách hóa đơn'
        # Mỗi phòng chỉ 1 hóa đơn/tháng (BR-02)
        unique_together = [('room', 'billing_month')]
        ordering = ['-billing_month']


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
