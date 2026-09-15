# RTMS — Implementation Status Report

**Ngày:** 15/09/2026  
**Nhóm:** GROUP5_PTTKHT  
**Hệ thống:** Rental/Room Tenant Management System (RTMS)

---

## Ket qua tong quan

| Epic | User Story | Ten chuc nang | Trang thai |
|------|-----------|---------------|-----------|
| EPIC 1 | **US01** | Quan ly thong tin phong (CRUD) | HOAN THANH |
| EPIC 1 | **US02** | Cap nhat trang thai phong | HOAN THANH |
| EPIC 2 | **US03** | Ghi nhan chi so dien/nuoc | HOAN THANH |
| EPIC 2 | **US04** | Quan ly phu phi dich vu (rac, internet) | HOAN THANH |
| EPIC 2 | **US05** | Tinh toan & xem truoc hoa don | HOAN THANH |

---

## EPIC 1 - Quan ly Phong Tro

### US01 - CRUD Phong

| Acceptance Criteria | Trang thai | Ghi chu |
|---------------------|-----------|---------|
| E1.1 Chu tro them phong moi voi day du truong | OK | Form room_form.html voi validation |
| E1.2 Validate ten phong chi la so | OK | _validate_room_name() trong views.py |
| E1.3 Validate so dau ten phong = so tang | OK | Business Rule BR-00 trong view |
| E1.4 Card nguoi thue enable/disable theo status | OK | JS updateTenantCard() trong room_form.html |
| E1.5 Khong the xoa phong dang co nguoi thue | OK | Room.can_delete property + BR-01 |
| E1.6 Sua thong tin phong | OK | room_edit() view |
| E1.7 Ngay nhan phong khong duoc la qua khu | OK | Validation trong view + min HTML attr |

### US02 - Cap nhat trang thai phong

| Acceptance Criteria | Trang thai | Ghi chu |
|---------------------|-----------|---------|
| E2.1 Chuyen trang thai: Trong -> Da coc/Dang thue | OK | room_status_update() view |
| E2.2 Chuyen trang thai: Dang thue -> Trong | OK | Inline form trong dashboard |
| E2.3 Phong sua chua khong cho thue | OK | Khong hien trong danh sach tenant |

---

## EPIC 2 - Quan ly Hoa Don

### US03 - Ghi nhan chi so dien, nuoc

| Acceptance Criteria | Trang thai | Ghi chu |
|---------------------|-----------|---------|
| E3.1 Nhap chi so dien/nuoc moi | OK | Form invoice_form.html |
| E3.2 Validate chi so moi >= chi so cu | OK | Server-side + client-side JS |
| E3.3 Chi so cu hien thi readonly | OK | input-readonly-block component |
| E3.4 Luu chi so cu vao Invoice | OK | old_electricity, old_water fields |
| E3.5 Sau khi tao hoa don, cap nhat chi so phong | OK | room.current_electricity = invoice.new_electricity |

### US04 - Phu phi dich vu

| Acceptance Criteria | Trang thai | Ghi chu |
|---------------------|-----------|---------|
| E4.1 Khai bao phi rac, phi internet tai phong | OK | trash_price, internet_price trong Room |
| E4.2 Phu phi tuy chon (extra_fee) | OK | extra_fee + extra_fee_reason trong Invoice |
| E4.3 Phi dich vu tu dong cong vao hoa don | OK | calculate_total() bao gom trash + internet |

### US05 - Xem truoc & Tao hoa don

| Acceptance Criteria | Trang thai | Ghi chu |
|---------------------|-----------|---------|
| E5.1 Xem truoc hoa don truoc khi xac nhan | OK | Real-time preview panel |
| E5.2 Tong = Phong + Dien + Nuoc + DV + Phu phi | OK | Invoice.calculate_total() |
| E5.3 Nguoi dung khong the sua tay tong tien | OK | Tong chi la text, khong co input |
| E5.4 Moi phong toi da 1 hoa don/thang | OK | unique_together = ('room', 'billing_month') |
| E5.5 Luu nhap hoac tao chinh thuc | OK | Hai nut: Tao hoa don va Luu nhap |

---

## Business Rules

| Rule | Mo ta | Trien khai |
|------|-------|-----------|
| **BR-00** | Chu so dau ten phong = so tang | Validate trong room_create / room_edit |
| **BR-01** | Khong xoa phong co trang thai != Trong/Sua chua | Room.can_delete property |
| **BR-02** | Moi phong chi co 1 hoa don/thang | unique_together = ('room', 'billing_month') |
| **BR-03** | Chi so dien/nuoc moi >= chi so cu | Server + client validation |
| **BR-04** | Ngay nhan phong khong duoc la qua khu | date.today() check + min HTML attr |

---

## Du lieu demo (Seed Data)

| Loai | Thong tin |
|------|----------|
| **Chu tro** | owner1 / demo1234 |
| **Nguoi thue 1** | tenant1 - Tran Thi Binh -> Phong 101 |
| **Nguoi thue 2** | tenant2 - Le Van Cuong -> Phong 102 |
| **Nguoi thue 3** | tenant3 - Pham Thi Dung -> Phong 201 |
| **Phong 101** | Dang thue - 3.000.000 d/thang - Tang 1 - 25.5 m2 |
| **Phong 102** | Da coc - 2.500.000 d/thang - Tang 1 - 20 m2 |
| **Phong 103** | Trong - 2.800.000 d/thang - Tang 1 - 22 m2 |
| **Phong 201** | Dang thue - 4.000.000 d/thang - Tang 2 - 30 m2 |
| **Phong 202** | Sua chua - 2.000.000 d/thang - Tang 2 - 18 m2 |
| **Phong 203** | Trong - 3.500.000 d/thang - Tang 2 - 26 m2 |
| **Hoa don mau** | Phong 101 - Thang 09/2026 - Tong: 3.535.000 d |

---

## Cach chay

```bash
# Cai dependencies
pip install django Pillow

# Khoi tao database
python manage.py migrate

# Seed du lieu demo
python seed_data.py

# Chay server
python manage.py runserver

# Truy cap: http://127.0.0.1:8000
# Dang nhap: owner1 / demo1234
```
