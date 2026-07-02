from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    if request.method == "POST":
        address = request.POST['address']
        phone = request.POST['phone']

        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total_amount=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price
            )

        cart_items.delete()

        return redirect('my_orders')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })


@login_required
def order_detail(request, id):
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    items = OrderItem.objects.filter(order=order)

    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items
    })