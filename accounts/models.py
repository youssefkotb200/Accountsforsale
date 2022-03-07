from django.db import models
# Create your models here.
from app.models import Categories
from User_Accounts.models import User

class Accounts(models.Model):
    buy_options = [
        ('sell-only', 'Sell Only'),
        ('sell-trade', 'Sell & Trade'),
        ('trade-only', 'Trade Only'),
    ]
    options = models.CharField(
        max_length=20,
        choices=buy_options,
    )
    title = models.CharField(max_length=30)
    account_img = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_avalabile = models.BooleanField(max_length=20, default=True)
    platform = models.CharField(max_length=20)
    approved = models.BooleanField(max_length=20, default=False)

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.title




class Review(models.Model):
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", default="1")
    review_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    stars_review = models.FloatField(default=0) 



class Trade_Requests(models.Model):
    account_owner = models.ForeignKey(User, on_delete=models.CASCADE, default="1")
    account_img = models.ImageField(null=True, blank=True, upload_to="images/")
    account_email = models.CharField(max_length=200, unique=True)
    account_password = models.CharField(max_length=200, unique=True)
    account_title = models.CharField(max_length=200)
    account_platform = models.CharField(max_length=200)
    trade_account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    approved = models.BooleanField(max_length=20, default=False)
    completed = models.BooleanField(max_length=20, default=False)
    answer = models.BooleanField(max_length=20, default=False)

    def __str__(self):
        return self.account_email
