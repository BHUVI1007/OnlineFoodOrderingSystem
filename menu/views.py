from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Food, Category


def menu(request):
    foods = Food.objects.filter(available=True)
    categories = Category.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')
    sort = request.GET.get('sort')

    if query:
        foods = foods.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category:
        foods = foods.filter(category__id=category)

    if sort == "low":
        foods = foods.order_by("price")
    elif sort == "high":
        foods = foods.order_by("-price")

    context = {
        "foods": foods,
        "categories": categories,
    }

    return render(request, "menu/menu.html", context)


def food_detail(request, id):
    food = get_object_or_404(Food, id=id)
    return render(request, "menu/food_detail.html", {"food": food})