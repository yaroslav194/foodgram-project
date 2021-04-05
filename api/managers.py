from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class PurchaseManager(models.Manager):
    def counter(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except Purchase.DoesNotExist:
            return 0

    def get_purchases_list(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except Purchase.DoesNotExist:
            return []

    def get_or_create_purchase(self, user):
        try:
            return super().get_queryset().get(user=user)
        except Purchase.DoesNotExist:
            purchase = Purchase(user=user)
            purchase.save()
            return purchase


class Purchase(models.Model):
    recipes = models.ManyToManyField(
        Recipe, related_name='purchases')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases')
    purchase = PurchaseManager()
