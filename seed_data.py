"""
Seed data cho demo RTMS
Tạo: 1 chủ trọ + 3 người thuê + 6 phòng ở các trạng thái khác nhau + 1 hóa đơn mẫu
"""
import os
import sys
import django
import json
from datetime import date, timedelta
from decimal import Decimal

# Fix encoding cho Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rtms.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile
from rooms.models import Room, TenantAssignment, Invoice


def create_seed_data():
    print("=== Bắt đầu seed data RTMS ===")

    # ============================================================
    # 1. Tạo chủ trọ (owner)
    # ============================================================
    if User.objects.filter(username='owner1').exists():
        print("Dữ liệu đã tồn tại. Xóa và tạo lại...")
        User.objects.filter(username__in=['owner1', 'tenant1', 'tenant2', 'tenant3']).delete()

    owner = User.objects.create_user(
        username='owner1',
        password='demo1234',
        first_name='Nguyễn',
        last_name='Văn An',
        email='owner@rtms.demo'
    )
    UserProfile.objects.create(user=owner, role='owner', phone='0901234567')
    print(f"  ✓ Tạo chủ trọ: owner1 / demo1234")

    # ============================================================
    # 2. Tạo người thuê
    # ============================================================
    t1 = User.objects.create_user(
        username='tenant1', password='demo1234',
        first_name='Trần', last_name='Thị Bình'
    )
    UserProfile.objects.create(user=t1, role='tenant', phone='0912345678', cccd='001234567890')

    t2 = User.objects.create_user(
        username='tenant2', password='demo1234',
        first_name='Lê', last_name='Văn Cường'
    )
    UserProfile.objects.create(user=t2, role='tenant', phone='0923456789', cccd='002345678901')

    t3 = User.objects.create_user(
        username='tenant3', password='demo1234',
        first_name='Phạm', last_name='Thị Dung'
    )
    UserProfile.objects.create(user=t3, role='tenant', phone='0934567890', cccd='003456789012')
    print(f"  ✓ Tạo 3 người thuê: tenant1, tenant2, tenant3")

    # ============================================================
    # 3. Tạo các phòng với trạng thái đa dạng
    # ============================================================
    rooms_data = [
        {
            'name': '101', 'floor': 1, 'area': Decimal('25.5'),
            'max_occupancy': 2,
            'amenities': json.dumps(['dieu_hoa', 'may_nuoc_nong', 'wifi']),
            'base_rent': Decimal('3000000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('20000'), 'internet_price': Decimal('100000'),
            'current_electricity': Decimal('1250'), 'current_water': Decimal('50'),
            'status': 'dang_thue',
        },
        {
            'name': '102', 'floor': 1, 'area': Decimal('20'),
            'max_occupancy': 1,
            'amenities': json.dumps(['may_nuoc_nong', 'wifi']),
            'base_rent': Decimal('2500000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('20000'), 'internet_price': Decimal('100000'),
            'current_electricity': Decimal('850'), 'current_water': Decimal('30'),
            'status': 'da_coc',
        },
        {
            'name': '103', 'floor': 1, 'area': Decimal('22'),
            'max_occupancy': 2,
            'amenities': json.dumps(['dieu_hoa', 'ban_cong']),
            'base_rent': Decimal('2800000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('20000'), 'internet_price': Decimal('100000'),
            'current_electricity': Decimal('0'), 'current_water': Decimal('0'),
            'status': 'trong',
        },
        {
            'name': '201', 'floor': 2, 'area': Decimal('30'),
            'max_occupancy': 3,
            'amenities': json.dumps(['dieu_hoa', 'tu_lanh', 'may_giat', 'wifi', 'noi_that']),
            'base_rent': Decimal('4000000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('25000'), 'internet_price': Decimal('120000'),
            'current_electricity': Decimal('2100'), 'current_water': Decimal('80'),
            'status': 'dang_thue',
        },
        {
            'name': '202', 'floor': 2, 'area': Decimal('18'),
            'max_occupancy': 1,
            'amenities': json.dumps(['may_nuoc_nong']),
            'base_rent': Decimal('2000000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('20000'), 'internet_price': Decimal('100000'),
            'current_electricity': Decimal('0'), 'current_water': Decimal('0'),
            'status': 'sua_chua',
        },
        {
            'name': '203', 'floor': 2, 'area': Decimal('26'),
            'max_occupancy': 2,
            'amenities': json.dumps(['dieu_hoa', 'may_nuoc_nong', 'ban_cong', 'wifi']),
            'base_rent': Decimal('3500000'),
            'electricity_price': Decimal('3500'), 'water_price': Decimal('15000'),
            'trash_price': Decimal('20000'), 'internet_price': Decimal('100000'),
            'current_electricity': Decimal('0'), 'current_water': Decimal('0'),
            'status': 'trong',
        },
    ]

    created_rooms = []
    for rd in rooms_data:
        room = Room.objects.create(owner=owner, **rd)
        created_rooms.append(room)
        print(f"  ✓ Tạo phòng {room.name} — {room.get_status_display()}")

    # ============================================================
    # 4. Gắn người thuê vào phòng "Đang thuê" và "Đã cọc"
    # ============================================================
    today = date.today()

    # Phòng 101 — Đang thuê — tenant1
    TenantAssignment.objects.create(
        room=created_rooms[0],
        tenant=t1,
        move_in_date=today,
        lease_duration=12,
        deposit=Decimal('3000000'),
    )
    print(f"  ✓ Gắn người thuê Trần Thị Bình → Phòng 101")

    # Phòng 102 — Đã cọc — tenant2
    TenantAssignment.objects.create(
        room=created_rooms[1],
        tenant=t2,
        move_in_date=today + timedelta(days=3),
        lease_duration=6,
        deposit=Decimal('2500000'),
    )
    print(f"  ✓ Gắn người thuê Lê Văn Cường → Phòng 102")

    # Phòng 201 — Đang thuê — tenant3
    TenantAssignment.objects.create(
        room=created_rooms[3],
        tenant=t3,
        move_in_date=today,
        lease_duration=24,
        deposit=Decimal('4000000'),
    )
    print(f"  ✓ Gắn người thuê Phạm Thị Dung → Phòng 201")

    # ============================================================
    # 5. Tạo hóa đơn mẫu cho phòng 101 (để demo invoice_list)
    # ============================================================
    room101 = created_rooms[0]
    billing = date(today.year, today.month, 1)
    new_elec = Decimal('1320')
    new_water = Decimal('58')

    inv = Invoice(
        room=room101,
        billing_month=billing,
        old_electricity=room101.current_electricity,
        new_electricity=new_elec,
        old_water=room101.current_water,
        new_water=new_water,
        base_rent=room101.base_rent,
        electricity_price=room101.electricity_price,
        water_price=room101.water_price,
        trash_price=room101.trash_price,
        internet_price=room101.internet_price,
        extra_fee=Decimal('50000'),
        extra_fee_reason='Phí sửa khóa cửa',
        status='chua_tt',
    )
    inv.total_amount = inv.calculate_total()
    inv.save()
    print(f"  ✓ Tạo hóa đơn mẫu Phòng 101 — {billing.strftime('%m/%Y')} — Tổng: {inv.total_amount:,} đ")

    print()
    print("=== SEED DATA HOÀN TẤT ===")
    print()
    print("THÔNG TIN ĐĂNG NHẬP DEMO:")
    print("  Chủ trọ:   owner1 / demo1234")
    print("  Người thuê: tenant1 / demo1234")
    print()
    print("URL truy cập: http://127.0.0.1:8000")


if __name__ == '__main__':
    create_seed_data()
