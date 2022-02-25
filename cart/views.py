from django.shortcuts import render
from django.urls import reverse
from .models import *
from accounts.models import Accounts 
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

def get_session(request):
    session = request.session.session_key
    if not session:
        session = request.session.create()
    return session


def cart(request):
    if request.user.is_authenticated:
        cartitem = CartItem.objects.filter(user_id=request.user).all()
    else:
        try:
            cart = Cart.objects.get(cart_id=get_session(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = get_session(request),
            )
            cart.save()
        cartitem = CartItem.objects.filter(cart_id=cart).all()
    Total_price = 0
    tax = 0
    Grand_total = 0
    for i in cartitem:
        Total_price += i.account_id.price
    tax = Total_price * 0.05
    Grand_total = Total_price + tax
    return render(request, 'cart/cart.html', {
        'cartitems': cartitem,
        'Total_price': Total_price,
        'tax': tax,
        'Grand_total': Grand_total,
    })


def add_to_cart(request, account_id):
    account = Accounts.objects.get(pk=int(account_id))
    if request.user.is_authenticated:
        cartitem = CartItem.objects.create(
            account_id = account,
            user_id = request.user
        )
    else:
        try:
            cart = Cart.objects.get(cart_id=get_session(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = get_session(request),
            )
            cart.save()
        cartitem = CartItem.objects.create(
            account_id = account,
            cart_id = cart
        )
    cartitem.save()
    return HttpResponseRedirect(reverse('cart'))



def remove_from_cart(request, account_id):
    account = Accounts.objects.get(pk=int(account_id))
    if request.user.is_authenticated:
        cartitem = CartItem.objects.get(Q(account_id=account) & Q(user_id=request.user)).delete()
    else:
        cart = Cart.objects.get(cart_id=get_session(request))
        cartitem = CartItem.objects.get(Q(account_id=account) & Q(cart_id=cart)).delete()
    return HttpResponseRedirect(reverse('cart'))

@login_required
def checkout(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "cart/checkout.html")