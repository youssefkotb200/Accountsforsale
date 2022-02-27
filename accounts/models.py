from django.db import models
# Create your models here.
from app.models import Categories
from User_Accounts.models import User

class Accounts(models.Model):
    buy_options = [
        ('sell', 'Sell Only'),
        ('sell-trade', 'Sell & Trade'),
        ('trade', 'Trade Only'),
    ]
    options = models.CharField(
        max_length=20,
        choices=buy_options,
    )
    title = models.CharField(max_length=30)
    account_img = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    options = models.CharField(max_length=30)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_avalabile = models.BooleanField(max_length=20, default=True)
    platform = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.title




class Review(models.Model):
    account_id = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    review_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True)
    stars_review = models.IntegerField() 