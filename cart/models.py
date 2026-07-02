from django.db import models
from django.contrib.auth.models import User
from menu.models import Food


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return self.food.price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"