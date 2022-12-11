from django import template
register = template.Library()

@register.filter(name='quantity')
def quantity(cart_items,food_id):
    for item in cart_items:
        if item.fooditem.id == food_id:
            return item.quantity
    return 0

@register.filter(name='itemid')
def itemid(cart_items,food_id):
    for item in cart_items:
        if item.fooditem.id == food_id:
            return item.id
    return 0
