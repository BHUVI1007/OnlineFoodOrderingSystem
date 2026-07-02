from django.shortcuts import render
from django.contrib.auth.models import User
from menu.models import Food
from orders.models import Order
from django.db.models import Sum

from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def dashboard(request):
    total_users = User.objects.count()
    total_foods = Food.objects.count()
    total_orders = Order.objects.count()

    revenue = Order.objects.aggregate(
        Sum('total_amount')
    )['total_amount__sum'] or 0

    pending = Order.objects.filter(status='Pending').count()
    delivered = Order.objects.filter(status='Delivered').count()

    context = {
        'users': total_users,
        'foods': total_foods,
        'orders': total_orders,
        'revenue': revenue,
        'pending': pending,
        'delivered': delivered,
    }

    return render(request, 'dashboard/dashboard.html', context)