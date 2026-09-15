"""
Custom template tags/filters cho app rooms
"""
from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def subtract(value, arg):
    """Trừ arg từ value"""
    try:
        return Decimal(str(value)) - Decimal(str(arg))
    except Exception:
        return 0


@register.filter
def format_vnd(value):
    """Format số thành VND không có ký hiệu đồng"""
    try:
        return f"{int(round(float(value))):,}".replace(',', '.')
    except Exception:
        return value


@register.filter
def get_item(dictionary, key):
    """Lấy giá trị từ dictionary theo key"""
    return dictionary.get(key, '')
