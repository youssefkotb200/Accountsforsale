from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import Accounts
from User_Accounts.models import User
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.account_id.title