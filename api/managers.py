from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class PurchaseManager(models.Manager):
    def counter(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.count()
        except models.ObjectDoesNotExist:
            return 0

    def get_purchases_list(self, user):
        try:
            return super().get_queryset().get(user=user).recipes.all()
        except models.ObjectDoesNotExist:
            return []

    def get_or_create_purchase(self, user):
        try:
            return super().get_queryset().get(user=user)
        except models.ObjectDoesNotExist:
            purchase = models(user=user)
            purchase.save()
            return purchase
