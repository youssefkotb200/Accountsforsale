from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateTimeField
# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    category_img = models.ImageField(null=True, blank=True, upload_to="category/")

    class Meta:
        verbose_name = 'Categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# class Trade_Requests(models.Model):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_info")
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     trade_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)



# class Trade(models.Model):
#     buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="trader")
#     seller = models.ForeignKey(User, on_delete=models.CASCADE)
#     buyer_account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="trader_account")
#     seller_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)



# class Transactions(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)
#     account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
#     bought_date = models.DateTimeField(auto_now_add=True)
