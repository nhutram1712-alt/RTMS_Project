from django.db.models import Q
"""
Views cho app rooms — CRUD phòng, tạo hóa đơn
Implement US01, US02, US03, US04, US05
"""
import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import (
    Room, TenantAssignment, Invoice, 
    MaintenanceRequest, Post, Message,
    AMENITY_CHOICES, ROOM_STATUS_CHOICES
)


# ============================================================
# HELPER: Validate số và độ dài
# ============================================================

def _validate_number(value, field_name, max_len=10, required=True, allow_decimal=True):
    """
    Validate một giá trị số:
    - Kiểm tra bắt buộc
    - Kiểm tra kiểu số
    - Kiểm tra độ dài tối đa
    Trả về (cleaned_value, error_message)
    """
    if not value and value != 0:
        if required:
            return None, f'Trường dữ liệu không được bỏ trống'
        return None, None

    value = str(value).strip()
    if not value:
        if required:
            return None, f'Trường dữ liệu không được bỏ trống'
        return None, None

    # Loại bỏ dấu phẩy nếu có
    clean = value.replace(',', '')

    # Kiểm tra độ dài (không tính dấu chấm thập phân)
    digits_only = clean.replace('.', '').replace('-', '')
    if len(digits_only) > max_len:
        return None, f'Độ dài nhập vào không hợp lệ (tối đa {max_len} chữ số)'

    try:
        result = Decimal(clean)
        return result, None
    except InvalidOperation:
        return None, 'Chỉ được phép nhập số'


def _validate_integer(value, field_name, max_len=10, required=True, min_val=1):
    """Validate số nguyên"""
    if not value and value != 0:
        if required:
            return None, f'Trường dữ liệu không được bỏ trống'
        return None, None

    value = str(value).strip()
    if not value:
        if required:
            return None, f'Trường dữ liệu không được bỏ trống'
        return None, None

    if len(value) > max_len:
        return None, f'Độ dài nhập vào không hợp lệ (tối đa {max_len} ký tự)'

    try:
        result = int(value)
        if result < min_val:
            return None, f'Giá trị phải lớn hơn hoặc bằng {min_val}'
        return result, None
    except (ValueError, TypeError):
        return None, 'Chỉ được phép nhập số nguyên'


# ============================================================
# US02 + Dashboard — Trang tổng quan
# ============================================================

@login_required
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

@login_required
def dashboard(request):
    """
    Trang tổng quan — hiển thị danh sách phòng của chủ trọ
    """
    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        return redirect('tenant_dashboard')
        
    rooms = Room.objects.filter(owner=request.user).order_by('name')
    context = {
        'rooms': rooms,
        'status_choices': ROOM_STATUS_CHOICES,
        'total_rooms': rooms.count(),
        'available_rooms': rooms.filter(status='trong').count(),
        'rented_rooms': rooms.filter(status__in=['dang_thue', 'da_coc']).count(),
        'repair_rooms': rooms.filter(status='sua_chua').count(),
    }
    return render(request, 'rooms/dashboard.html', context)


# ============================================================
# US01 — Tạo phòng mới
# ============================================================

@login_required
def room_create(request):
    """

    US01 — Form tạo phòng mới
    Validate đầy đủ theo SRS, xử lý tenant card toggle
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    tenants = User.objects.filter(profile__role='tenant', profile__owner=request.user)

    if request.method == 'POST':
        errors = {}
        data = {}

        # === Validate tên phòng ===
        name = request.POST.get('name', '').strip()
        if not name:
            errors['name'] = 'Tên phòng không được bỏ trống'
        elif not name.isdigit():
            errors['name'] = 'Tên phòng chỉ được chứa số'
        elif Room.objects.filter(name=name).exists():
            errors['name'] = f'Phòng {name} đã tồn tại!'
        else:
            data['name'] = name

        # === Validate tầng ===
        floor_raw = request.POST.get('floor', '').strip()
        if not floor_raw:
            errors['floor'] = 'Số tầng không được bỏ trống'
        elif not floor_raw.isdigit():
            errors['floor'] = 'Số tầng chỉ được phép nhập số'
        elif len(floor_raw) > 2:
            errors['floor'] = 'Số tầng không được vượt quá 2 chữ số!'
        else:
            floor_val = int(floor_raw)
            if floor_val < 0 or floor_val > 99:
                errors['floor'] = 'Số tầng không được vượt quá 2 chữ số!'
            else:
                data['floor'] = floor_val

        # === Validate diện tích ===
        area_val, area_err = _validate_number(request.POST.get('area', ''), 'Diện tích')
        if area_err:
            errors['area'] = area_err if area_err != 'Trường dữ liệu không được bỏ trống' else 'Diện tích không được bỏ trống'
        else:
            data['area'] = area_val

        # === Validate số người tối đa ===
        max_occ = request.POST.get('max_occupancy', '1')
        max_occ_val, max_occ_err = _validate_integer(max_occ, 'Số người tối đa', min_val=1)
        if max_occ_err:
            errors['max_occupancy'] = max_occ_err
        else:
            data['max_occupancy'] = max_occ_val or 1

        # === Validate giá thuê ===
        base_rent_val, base_rent_err = _validate_number(request.POST.get('base_rent', ''), 'Giá thuê')
        if base_rent_err:
            errors['base_rent'] = base_rent_err
        else:
            data['base_rent'] = base_rent_val

        # === Validate đơn giá điện ===
        elec_val, elec_err = _validate_number(request.POST.get('electricity_price', ''), 'Đơn giá điện')
        if elec_err:
            errors['electricity_price'] = elec_err
        else:
            data['electricity_price'] = elec_val

        # === Validate đơn giá nước ===
        water_val, water_err = _validate_number(request.POST.get('water_price', ''), 'Đơn giá nước')
        if water_err:
            errors['water_price'] = water_err
        else:
            data['water_price'] = water_val

        # === Validate chỉ số điện đầu (không bắt buộc) ===
        cur_elec_raw = request.POST.get('current_electricity', '').strip()
        if cur_elec_raw:
            cur_elec_val, cur_elec_err = _validate_number(cur_elec_raw, 'Chỉ số điện đầu', required=False)
            if cur_elec_err:
                errors['current_electricity'] = cur_elec_err
            else:
                data['current_electricity'] = cur_elec_val
        else:
            data['current_electricity'] = 0

        # === Validate chỉ số nước đầu (không bắt buộc) ===
        cur_water_raw = request.POST.get('current_water', '').strip()
        if cur_water_raw:
            cur_water_val, cur_water_err = _validate_number(cur_water_raw, 'Chỉ số nước đầu', required=False)
            if cur_water_err:
                errors['current_water'] = cur_water_err
            else:
                data['current_water'] = cur_water_val
        else:
            data['current_water'] = 0

        # === Validate phí rác (US04) ===
        trash_val, trash_err = _validate_number(request.POST.get('trash_price', ''), 'Rác')
        if trash_err:
            if 'không hợp lệ' in trash_err:
                errors['trash_price'] = 'Rác không hợp lệ'
            elif 'nhập số' in trash_err:
                errors['trash_price'] = 'Rác chỉ được phép nhập số'
            else:
                errors['trash_price'] = trash_err
        else:
            data['trash_price'] = trash_val

        # === Validate phí internet (US04) ===
        inet_val, inet_err = _validate_number(request.POST.get('internet_price', ''), 'Internet')
        if inet_err:
            if 'không hợp lệ' in inet_err:
                errors['internet_price'] = 'Internet không hợp lệ'
            elif 'nhập số' in inet_err:
                errors['internet_price'] = 'Internet chỉ được phép nhập số'
            else:
                errors['internet_price'] = inet_err
        else:
            data['internet_price'] = inet_val

        # === Trạng thái phòng ===
        status = request.POST.get('status', 'trong')
        valid_statuses = [s[0] for s in ROOM_STATUS_CHOICES]
        if status not in valid_statuses:
            status = 'trong'
        data['status'] = status

        # === Tiện nghi ===
        amenities = request.POST.getlist('amenities')
        data['amenities'] = json.dumps(amenities)

        # === Validate thông tin người thuê nếu cần ===
        tenant_data = {}
        if status in ('dang_thue', 'da_coc'):
            # Tenant card ENABLE — bắt buộc nhập
            tenant_id = request.POST.get('tenant_id', '').strip()
            if not tenant_id:
                errors['tenant_id'] = 'Vui lòng chọn người thuê'
            else:
                try:
                    tenant_obj = User.objects.get(id=tenant_id, profile__role='tenant')
                    tenant_data['tenant'] = tenant_obj
                except User.DoesNotExist:
                    errors['tenant_id'] = 'Người thuê không hợp lệ'

            # Ngày nhận phòng — không được chọn ngày quá khứ
            move_in_raw = request.POST.get('move_in_date', '').strip()
            if not move_in_raw:
                errors['move_in_date'] = 'Ngày nhận phòng không được bỏ trống'
            else:
                try:
                    move_in = datetime.strptime(move_in_raw, '%Y-%m-%d').date()
                    if move_in < date.today():
                        errors['move_in_date'] = 'Không thể chọn ngày nhận phòng trong quá khứ'
                    else:
                        tenant_data['move_in_date'] = move_in
                except ValueError:
                    errors['move_in_date'] = 'Định dạng ngày không hợp lệ'

            # Thời hạn thuê
            lease_raw = request.POST.get('lease_duration', '').strip()
            if not lease_raw:
                errors['lease_duration'] = 'Thời hạn thuê phòng không được bỏ trống'
            else:
                try:
                    lease_val = int(lease_raw)
                    if lease_val <= 0:
                        errors['lease_duration'] = 'Thời hạn thuê phòng không được nhập số âm'
                    elif len(lease_raw) > 10:
                        errors['lease_duration'] = 'Độ dài nhập vào của thời hạn thuê không phù hợp'
                    else:
                        tenant_data['lease_duration'] = lease_val
                except ValueError:
                    errors['lease_duration'] = 'Thời hạn thuê phòng chỉ được phép nhập số'

            # Tiền cọc
            deposit_raw = request.POST.get('deposit', '').strip()
            if not deposit_raw:
                errors['deposit'] = 'Tiền cọc không được bỏ trống'
            else:
                try:
                    deposit_val = Decimal(deposit_raw)
                    if deposit_val <= 0:
                        errors['deposit'] = 'Tiền cọc không được bằng 0'
                    elif len(deposit_raw.replace('.', '').replace(',', '')) > 10:
                        errors['deposit'] = 'Độ dài nhập vào của tiền cọc không phù hợp'
                    else:
                        tenant_data['deposit'] = deposit_val
                except InvalidOperation:
                    errors['deposit'] = 'Tiền cọc chỉ được phép nhập số'

            # Ảnh hợp đồng (optional)
            if 'contract_image' in request.FILES:
                tenant_data['contract_image'] = request.FILES['contract_image']

        # === Nếu không có lỗi thì lưu ===
        if not errors:
            room = Room.objects.create(owner=request.user, **data)

            # Lưu thông tin người thuê nếu có
            if tenant_data and status in ('dang_thue', 'da_coc'):
                TenantAssignment.objects.create(room=room, **tenant_data)

            messages.success(request, f'Đã thêm phòng {room.name} thành công!')
            return redirect('dashboard')

        # Có lỗi — render lại form với thông báo lỗi
        context = {
            'errors': errors,
            'post_data': request.POST,
            'amenity_choices': AMENITY_CHOICES,
            'status_choices': ROOM_STATUS_CHOICES,
            'tenants': tenants,
            'selected_amenities': request.POST.getlist('amenities'),
            'today_str': date.today().isoformat(),
            'room': None,
        }
        return render(request, 'rooms/room_form.html', context)

    # GET — form trống
    context = {
        'amenity_choices': AMENITY_CHOICES,
        'status_choices': ROOM_STATUS_CHOICES,
        'tenants': tenants,
        'selected_amenities': [],
        'today_str': date.today().isoformat(),
        'room': None,
    }
    return render(request, 'rooms/room_form.html', context)


# ============================================================
# US01 — Sửa phòng
# ============================================================

@login_required
def room_edit(request, room_id):
    """

    US01 — Form sửa thông tin phòng
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id, owner=request.user)
    tenants = User.objects.filter(profile__role='tenant', profile__owner=request.user)

    # Lấy thông tin người thuê hiện tại (nếu có)
    try:
        assignment = room.tenant_assignment
    except TenantAssignment.DoesNotExist:
        assignment = None

    if request.method == 'POST':
        errors = {}
        data = {}

        # === Validate tên phòng ===
        name = request.POST.get('name', '').strip()
        if not name:
            errors['name'] = 'Tên phòng không được bỏ trống'
        elif not name.isdigit():
            errors['name'] = 'Tên phòng chỉ được chứa số'
        elif Room.objects.filter(name=name).exclude(id=room_id).exists():
            errors['name'] = f'Phòng {name} đã tồn tại!'
        else:
            data['name'] = name

        # === Validate tầng ===
        floor_raw = request.POST.get('floor', '').strip()
        if not floor_raw:
            errors['floor'] = 'Số tầng không được bỏ trống'
        elif not floor_raw.isdigit():
            errors['floor'] = 'Số tầng chỉ được phép nhập số'
        elif len(floor_raw) > 2:
            errors['floor'] = 'Số tầng không được vượt quá 2 chữ số!'
        else:
            floor_val = int(floor_raw)
            if floor_val > 99:
                errors['floor'] = 'Số tầng không được vượt quá 2 chữ số!'
            else:
                data['floor'] = floor_val

        # Validate các trường số (tái sử dụng logic từ room_create)
        area_val, area_err = _validate_number(request.POST.get('area', ''), 'Diện tích')
        if area_err:
            errors['area'] = area_err if area_err != 'Trường dữ liệu không được bỏ trống' else 'Diện tích không được bỏ trống'
        else:
            data['area'] = area_val

        max_occ = request.POST.get('max_occupancy', '1')
        max_occ_val, max_occ_err = _validate_integer(max_occ, 'Số người tối đa', min_val=1)
        if max_occ_err:
            errors['max_occupancy'] = max_occ_err
        else:
            data['max_occupancy'] = max_occ_val or 1

        base_rent_val, base_rent_err = _validate_number(request.POST.get('base_rent', ''), 'Giá thuê')
        if base_rent_err:
            errors['base_rent'] = base_rent_err
        else:
            data['base_rent'] = base_rent_val

        elec_val, elec_err = _validate_number(request.POST.get('electricity_price', ''), 'Đơn giá điện')
        if elec_err:
            errors['electricity_price'] = elec_err
        else:
            data['electricity_price'] = elec_val

        water_val, water_err = _validate_number(request.POST.get('water_price', ''), 'Đơn giá nước')
        if water_err:
            errors['water_price'] = water_err
        else:
            data['water_price'] = water_val

        cur_elec_raw = request.POST.get('current_electricity', '').strip()
        if cur_elec_raw:
            cur_elec_val, cur_elec_err = _validate_number(cur_elec_raw, 'Chỉ số điện', required=False)
            if cur_elec_err:
                errors['current_electricity'] = cur_elec_err
            else:
                data['current_electricity'] = cur_elec_val
        else:
            data['current_electricity'] = 0

        cur_water_raw = request.POST.get('current_water', '').strip()
        if cur_water_raw:
            cur_water_val, cur_water_err = _validate_number(cur_water_raw, 'Chỉ số nước', required=False)
            if cur_water_err:
                errors['current_water'] = cur_water_err
            else:
                data['current_water'] = cur_water_val
        else:
            data['current_water'] = 0

        # Validate phí rác và internet (US04)
        trash_val, trash_err = _validate_number(request.POST.get('trash_price', ''), 'Rác')
        if trash_err:
            errors['trash_price'] = 'Rác không hợp lệ' if 'hợp lệ' in trash_err else ('Rác chỉ được phép nhập số' if 'số' in trash_err else trash_err)
        else:
            data['trash_price'] = trash_val

        inet_val, inet_err = _validate_number(request.POST.get('internet_price', ''), 'Internet')
        if inet_err:
            errors['internet_price'] = 'Internet không hợp lệ' if 'hợp lệ' in inet_err else ('Internet chỉ được phép nhập số' if 'số' in inet_err else inet_err)
        else:
            data['internet_price'] = inet_val

        status = request.POST.get('status', 'trong')
        valid_statuses = [s[0] for s in ROOM_STATUS_CHOICES]
        if status not in valid_statuses:
            status = 'trong'
        data['status'] = status

        amenities = request.POST.getlist('amenities')
        data['amenities'] = json.dumps(amenities)

        # Validate thông tin người thuê
        tenant_data = {}
        if status in ('dang_thue', 'da_coc'):
            tenant_id = request.POST.get('tenant_id', '').strip()
            if not tenant_id:
                errors['tenant_id'] = 'Vui lòng chọn người thuê'
            else:
                try:
                    tenant_obj = User.objects.get(id=tenant_id, profile__role='tenant')
                    tenant_data['tenant'] = tenant_obj
                except User.DoesNotExist:
                    errors['tenant_id'] = 'Người thuê không hợp lệ'

            move_in_raw = request.POST.get('move_in_date', '').strip()
            if not move_in_raw:
                errors['move_in_date'] = 'Ngày nhận phòng không được bỏ trống'
            else:
                try:
                    move_in = datetime.strptime(move_in_raw, '%Y-%m-%d').date()
                    if move_in < date.today():
                        errors['move_in_date'] = 'Không thể chọn ngày nhận phòng trong quá khứ'
                    else:
                        tenant_data['move_in_date'] = move_in
                except ValueError:
                    errors['move_in_date'] = 'Định dạng ngày không hợp lệ'

            lease_raw = request.POST.get('lease_duration', '').strip()
            if not lease_raw:
                errors['lease_duration'] = 'Thời hạn thuê phòng không được bỏ trống'
            else:
                try:
                    lease_val = int(lease_raw)
                    if lease_val <= 0:
                        errors['lease_duration'] = 'Thời hạn thuê phòng không được nhập số âm'
                    elif len(lease_raw) > 10:
                        errors['lease_duration'] = 'Độ dài nhập vào của thời hạn thuê không phù hợp'
                    else:
                        tenant_data['lease_duration'] = lease_val
                except ValueError:
                    errors['lease_duration'] = 'Thời hạn thuê phòng chỉ được phép nhập số'

            deposit_raw = request.POST.get('deposit', '').strip()
            if not deposit_raw:
                errors['deposit'] = 'Tiền cọc không được bỏ trống'
            else:
                try:
                    deposit_val = Decimal(deposit_raw)
                    if deposit_val <= 0:
                        errors['deposit'] = 'Tiền cọc không được bằng 0'
                    else:
                        tenant_data['deposit'] = deposit_val
                except InvalidOperation:
                    errors['deposit'] = 'Tiền cọc chỉ được phép nhập số'

            if 'contract_image' in request.FILES:
                tenant_data['contract_image'] = request.FILES['contract_image']

        if not errors:
            # Cập nhật room
            for field, value in data.items():
                setattr(room, field, value)
            room.save()

            # Cập nhật thông tin người thuê
            if status in ('dang_thue', 'da_coc') and tenant_data:
                if assignment:
                    for field, value in tenant_data.items():
                        setattr(assignment, field, value)
                    assignment.save()
                else:
                    TenantAssignment.objects.create(room=room, **tenant_data)
            elif status in ('trong', 'sua_chua') and assignment:
                # Xóa thông tin người thuê khi phòng trống hoặc sửa chữa
                assignment.delete()

            messages.success(request, f'Đã cập nhật phòng {room.name} thành công!')
            return redirect('dashboard')

        context = {
            'room': room,
            'assignment': assignment,
            'errors': errors,
            'post_data': request.POST,
            'amenity_choices': AMENITY_CHOICES,
            'status_choices': ROOM_STATUS_CHOICES,
            'tenants': tenants,
            'selected_amenities': request.POST.getlist('amenities'),
            'is_edit': True,
            'today_str': date.today().isoformat(),
        }
        return render(request, 'rooms/room_form.html', context)

    # GET — điền dữ liệu sẵn
    context = {
        'room': room,
        'assignment': assignment,
        'amenity_choices': AMENITY_CHOICES,
        'status_choices': ROOM_STATUS_CHOICES,
        'tenants': tenants,
        'selected_amenities': room.get_amenities_list(),
        'is_edit': True,
        'today_str': date.today().isoformat(),
    }
    return render(request, 'rooms/room_form.html', context)


# ============================================================
# US01 — Xóa phòng
# ============================================================

@login_required
@require_POST
def room_delete(request, room_id):
    """

    US01 — Xóa phòng
    Không cho xóa nếu đang thuê hoặc đã cọc (BR-01)
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id, owner=request.user)

    if not room.can_delete():
        messages.error(request, f'Không thể xóa phòng {room.name} vì đang có người thuê!')
        return redirect('dashboard')

    room_name = room.name
    room.delete()
    messages.success(request, f'Đã xóa phòng {room_name} thành công!')
    return redirect('dashboard')


# ============================================================
# US02 — Cập nhật trạng thái nhanh (AJAX)
# ============================================================

@login_required
@require_POST
def room_status_update(request, room_id):
    """

    US02 — Cập nhật trạng thái phòng nhanh từ dashboard
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id, owner=request.user)
    new_status = request.POST.get('status', '').strip()

    valid_statuses = [s[0] for s in ROOM_STATUS_CHOICES]
    if new_status not in valid_statuses:
        messages.error(request, 'Trạng thái không hợp lệ!')
        return redirect('dashboard')

    old_status = room.status
    room.status = new_status
    room.save()

    # Nếu chuyển sang Trống/Sửa chữa thì xóa thông tin người thuê
    if new_status in ('trong', 'sua_chua'):
        try:
            room.tenant_assignment.delete()
        except TenantAssignment.DoesNotExist:
            pass

    status_display = dict(ROOM_STATUS_CHOICES).get(new_status, new_status)
    messages.success(request, f'Đã cập nhật trạng thái phòng {room.name} thành "{status_display}"')
    return redirect('dashboard')


# ============================================================
# US03 + US04 + US05 — Tạo hóa đơn
# ============================================================

@login_required
def invoice_create(request, room_id):
    """

    US03/US04/US05 — Trang tạo hóa đơn cho một phòng
    - Hiển thị readonly thông tin phòng
    - Nhập chỉ số điện/nước mới
    - Tính tổng tự động
    - Validate trùng hóa đơn cùng tháng (BR-02)
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id, owner=request.user)
    today = date.today()
    # Billing month = tháng hiện tại (ngày đầu tháng)
    billing_month = date(today.year, today.month, 1)

    # Kiểm tra đã có hóa đơn tháng này chưa (BR-02)
    existing_invoice = Invoice.objects.filter(room=room, billing_month=billing_month).first()

    if request.method == 'POST':
        errors = {}
        action = request.POST.get('action', 'create')  # 'create' hoặc 'draft'

        # Chỉ số điện cũ (readonly từ room)
        old_elec = room.current_electricity or Decimal('0')
        old_water = room.current_water or Decimal('0')

        # === Validate chỉ số điện mới (US03) ===
        new_elec_raw = request.POST.get('new_electricity', '').strip()
        if not new_elec_raw:
            errors['new_electricity'] = 'Trường dữ liệu không được bỏ trống'
        else:
            if len(new_elec_raw.replace('.', '').replace(',', '')) > 10:
                errors['new_electricity'] = 'Độ dài không hợp lệ'
            else:
                try:
                    new_elec = Decimal(new_elec_raw)
                    if new_elec < old_elec:
                        errors['new_electricity'] = f'Chỉ số điện mới phải lớn hơn hoặc bằng chỉ số cũ ({old_elec})'
                except InvalidOperation:
                    errors['new_electricity'] = 'please enter a number'

        # === Validate chỉ số nước mới (US03) ===
        new_water_raw = request.POST.get('new_water', '').strip()
        if not new_water_raw:
            errors['new_water'] = 'Trường dữ liệu không được bỏ trống'
        else:
            if len(new_water_raw.replace('.', '').replace(',', '')) > 10:
                errors['new_water'] = 'Độ dài không hợp lệ'
            else:
                try:
                    new_water = Decimal(new_water_raw)
                    if new_water < old_water:
                        errors['new_water'] = f'Chỉ số nước mới phải lớn hơn hoặc bằng chỉ số cũ ({old_water})'
                except InvalidOperation:
                    errors['new_water'] = 'please enter a number'

        # === Validate phụ phí (optional, US03) ===
        extra_fee_raw = request.POST.get('extra_fee', '').strip()
        extra_fee = Decimal('0')
        if extra_fee_raw:
            if len(extra_fee_raw.replace('.', '').replace(',', '')) > 10:
                errors['extra_fee'] = 'Độ dài Phụ phí không hợp lệ'
            else:
                try:
                    extra_fee = Decimal(extra_fee_raw)
                except InvalidOperation:
                    errors['extra_fee'] = 'Phụ phí chỉ được phép nhập số hợp lệ'

        extra_fee_reason = request.POST.get('extra_fee_reason', '').strip()

        # Kiểm tra trùng hóa đơn cùng tháng (BR-02)
        if not errors and action == 'create':
            if existing_invoice and existing_invoice.status != 'nhap':
                errors['duplicate'] = f'Phòng {room.name} đã có hóa đơn tháng {billing_month.strftime("%m/%Y")}!'

        if not errors:
            # Tính tổng tiền (US05)
            new_elec = Decimal(new_elec_raw)
            new_water = Decimal(new_water_raw)

            # Xác định status invoice
            invoice_status = 'chua_tt' if action == 'create' else 'nhap'

            # Nếu đã có invoice nháp thì cập nhật, không thì tạo mới
            if existing_invoice and existing_invoice.status == 'nhap':
                inv = existing_invoice
            else:
                inv = Invoice(room=room, billing_month=billing_month)

            inv.old_electricity = old_elec
            inv.new_electricity = new_elec
            inv.old_water = old_water
            inv.new_water = new_water
            inv.base_rent = room.base_rent
            inv.electricity_price = room.electricity_price
            inv.water_price = room.water_price
            inv.trash_price = room.trash_price
            inv.internet_price = room.internet_price
            inv.extra_fee = extra_fee
            inv.extra_fee_reason = extra_fee_reason
            inv.status = invoice_status
            inv.total_amount = inv.calculate_total()
            inv.save()

            # Cập nhật chỉ số điện nước mới vào room (để làm chỉ số đầu kỳ sau)
            if action == 'create':
                room.current_electricity = new_elec
                room.current_water = new_water
                room.save()

            if action == 'create':
                messages.success(request, f'Đã tạo hóa đơn tháng {billing_month.strftime("%m/%Y")} cho phòng {room.name}!')
            else:
                messages.success(request, f'Đã lưu nháp hóa đơn tháng {billing_month.strftime("%m/%Y")} cho phòng {room.name}!')
            return redirect('dashboard')

        # Render lại form nếu có lỗi
        context = {
            'room': room,
            'billing_month': billing_month,
            'old_electricity': old_elec,
            'old_water': old_water,
            'errors': errors,
            'post_data': request.POST,
            'existing_invoice': existing_invoice,
        }
        return render(request, 'rooms/invoice_form.html', context)

    # GET
    old_elec = room.current_electricity or Decimal('0')
    old_water = room.current_water or Decimal('0')
    context = {
        'room': room,
        'billing_month': billing_month,
        'old_electricity': old_elec,
        'old_water': old_water,
        'existing_invoice': existing_invoice,
    }
    return render(request, 'rooms/invoice_form.html', context)


@login_required
def invoice_list(request):
    """

    Danh sách hóa đơn của tất cả phòng thuộc chủ trọ
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    rooms = Room.objects.filter(owner=request.user)
    invoices = Invoice.objects.filter(room__in=rooms).select_related('room').order_by('-billing_month')
    context = {'invoices': invoices}
    return render(request, 'rooms/invoice_list.html', context)


@login_required
def invoice_detail(request, invoice_id):
    """
    Chi tiết một hóa đơn
    """
    rooms = Room.objects.filter(owner=request.user)
    invoice = get_object_or_404(Invoice, id=invoice_id, room__in=rooms)
    context = {'invoice': invoice}
    return render(request, 'rooms/invoice_detail.html', context)


# ============================================================
# AJAX — Tính tiền preview real-time (US05)
# ============================================================

@login_required
def calculate_invoice_preview(request, room_id):
    """

    AJAX endpoint — tính preview tổng tiền theo công thức US05
    Được gọi khi người dùng nhập số liệu trên form
    """

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

    room = get_object_or_404(Room, id=room_id, owner=request.user)

    try:
        old_elec = room.current_electricity or Decimal('0')
        old_water = room.current_water or Decimal('0')
        new_elec = Decimal(request.GET.get('new_electricity', '0') or '0')
        new_water = Decimal(request.GET.get('new_water', '0') or '0')
        extra_fee = Decimal(request.GET.get('extra_fee', '0') or '0')

        # Tính từng khoản
        electricity_cost = max(Decimal('0'), (new_elec - old_elec)) * room.electricity_price
        water_cost = max(Decimal('0'), (new_water - old_water)) * room.water_price
        service_cost = room.trash_price + room.internet_price
        total = room.base_rent + electricity_cost + water_cost + service_cost + extra_fee

        return JsonResponse({
            'success': True,
            'base_rent': float(room.base_rent),
            'electricity_cost': float(electricity_cost),
            'water_cost': float(water_cost),
            'service_cost': float(service_cost),
            'extra_fee': float(extra_fee),
            'total': float(round(total, 0)),
        })
    except (InvalidOperation, ValueError):
        return JsonResponse({'success': False, 'error': 'Dữ liệu không hợp lệ'})

    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.urls import reverse

@login_required
@require_POST
def invoice_send_email(request, invoice_id):

    if not hasattr(request.user, 'profile') or not request.user.profile.is_owner():
        from django.contrib import messages
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('tenant_dashboard')

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
        message = f"Xin chào {tenant.get_full_name() or tenant.username},\n\nHóa đơn tháng {invoice.billing_month.strftime('%m/%Y')} cho Phòng {invoice.room.name} của bạn chưa được thanh toán.\nTổng số tiền: {int(invoice.total_amount):,} VNĐ.\n\nVui lòng thanh toán qua số tài khoản: 123456789 (Ngân hàng VCB - Chủ tài khoản: Chủ trọ demo).\nMã tra cứu hóa đơn của bạn: HD{invoice.id:04d}.\nBạn có thể xem chi tiết tại hệ thống RTMS.\n\nTrân trọng,\nQuản lý dãy trọ."
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

