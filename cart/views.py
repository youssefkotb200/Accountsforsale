from django.shortcuts import render
from django.urls import reverse
from .models import *
from accounts.models import Accounts 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests
from .models import Order, Payment, OrderProduct
import json
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

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
        "count": cartitem.count()
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
    cartitem = CartItem.objects.filter(user_id=request.user).all()
    Total_price = 0
    tax = 0
    Grand_total = 0
    for i in cartitem:
        Total_price += i.account_id.price
    tax = Total_price * 0.05
    Grand_total = Total_price + tax
    if request.method == "POST":
            user = request.user
            data = Order()
            data.user = user
            data.order_total = Grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=user, is_ordered=False, order_number=order_number)
            return render(request, 'cart/payment.html', {
                'cartitems': cartitem,
                'Total_price': Total_price,
                'tax': tax,
                'Grand_total': Grand_total,
                "order": order
            })
    else:
        return render(request, 'cart/checkout.html', {
            'cartitems': cartitem,
            'Total_price': Total_price,
            'tax': tax,
            'Grand_total': Grand_total,
        })


@login_required
def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to Order Product table
    cart_items = CartItem.objects.filter(user_id=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order = order
        orderproduct.account = item.account_id
        orderproduct.save()
        account = Accounts.objects.get(id=item.account_id.id)
        account.is_avalabile = False
        account.save()

    # Clear cart
    CartItem.objects.filter(user_id=request.user).delete()

    # Send order recieved email to customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('cart/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse
    data = {}
    return JsonResponse(data)


@login_required
def order_completed(request, order_number):
    order = Order.objects.get(user=request.user, is_ordered=True, order_number=order_number)
    orderproducts = OrderProduct.objects.filter(order=order).all()
    Total_price = 0
    tax = 0
    Grand_total = 0
    for i in orderproducts:
        Total_price += i.account.price
        user = User.objects.get(pk=i.account.owner.id)
        user.wallet += i.account.price
        user.save()
        mail_subject = 'Your Account have been sold'
        message = render_to_string('cart/account_sold.html', {
            'user': user,
            'account': i.account,
        })
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()


    tax = Total_price * 0.05
    Grand_total = Total_price + tax
    return render(request, "cart/order_completed.html", {
        "order": order,
        "orderproducts": orderproducts,
        'Total_price': Total_price,
        'tax': tax,
        'Grand_total': Grand_total,
    })