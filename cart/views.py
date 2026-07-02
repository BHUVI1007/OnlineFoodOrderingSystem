from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart
from menu.models import Food


@login_required
def add_to_cart(request, food_id):
    food = get_object_or_404(Food, id=food_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.total_price for item in items)

    return render(request, 'cart/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def remove_cart(request, id):
    item = get_object_or_404(Cart, id=id)
    item.delete()
    return redirect('view_cart')


@login_required
def increase_quantity(request, id):
    item = get_object_or_404(Cart, id=id)
    item.quantity += 1
    item.save()
    return redirect('view_cart')


@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(Cart, id=id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('view_cart')