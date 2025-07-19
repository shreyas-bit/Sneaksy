# shop/templatetags/cart_extras.py
from django import template

register = template.Library()

@register.filter
def sum_total(items):
    return sum(item.product.price * item.quantity for item in items)

@register.filter
def multiply(price, quantity):
    return price * quantity