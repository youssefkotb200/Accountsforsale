from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Payment, Order, OrderProduct
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Accounts, Trade_Requests
from accounts.views import pagination, averageReview
from django.contrib import messages, auth
from app.models import Categories
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).all()[:6]
    return render(request,"dashboard/dashboard.html", {
        "orders": orders,
    })

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).all()
    return render(request,"dashboard/dashboard.html", {
        "orders": orders,
    })

@login_required
def selling_accounts(request):
    accounts = Accounts.objects.filter(owner=request.user, is_avalabile=True).all()
    return render(request,"dashboard/selling_accounts.html", {
        'page_obj': pagination(request.GET.get('page'), accounts),
    })

@login_required
def sold_accounts(request):
    accounts = Accounts.objects.filter(owner=request.user, is_avalabile=False).all()
    return render(request,"dashboard/selling_accounts.html", {
        'page_obj': pagination(request.GET.get('page'), accounts),
    })

@login_required
def profile(request):
    return render(request,"dashboard/profile.html", {
        "user": request.user,
        'rating': averageReview(request.user.id)
    })


@login_required
def order(request, order_number):
    orders = Order.objects.get(user=request.user, is_ordered=True, order_number=order_number)
    orderproducts = OrderProduct.objects.filter(order=orders).all()
    return render(request,"dashboard/order.html", {
        'page_obj': pagination(request.GET.get('page'), orderproducts),

    })



@login_required
def add_account(request):
    account_email = request.POST['email']
    account_password = request.POST['password']
    account_price = request.POST['price']
    account_category = request.POST['category']
    account_options = request.POST['options']
    account_title = request.POST['title']
    if not account_email:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if not account_password:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if Accounts.objects.filter(email=account_email).exists():
        messages.error(request, 'Email already exists')
        return redirect('/dashboard/selling_accounts')

    if Accounts.objects.filter(password=account_password).exists():
        messages.error(request, 'password already exists')
        return redirect('/dashboard/selling_accounts')

    if not account_price.isdigit():
        messages.error(request, 'price must be a number')
        return redirect('/dashboard/selling_accounts')

    if not account_price:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if not account_category:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if not account_options:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if not account_title:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')

    if request.FILES:
        account_image = request.FILES['image']
    else:
        messages.error(request, 'all fields is required')
        return redirect('/dashboard/selling_accounts')
    

    account = Accounts.objects.create(
        options=account_options,
        title=account_title,
        account_img=account_image,
        price=account_price,
        owner=request.user,
        email=account_email,
        password=account_password,
        category=Categories.objects.get(slug=account_category),
        platform=account_category
    )
    account.save()
    messages.success(request, 'Your Account have been  recived, within two days your account will be reviwed')
    return redirect('/dashboard/selling_accounts')




def delete_account(request, acc_id):
    try:
        account = Accounts.objects.get(pk=acc_id)
    except Accounts.DoesNotExists:
        messages.error(request, 'is not found')
    account.delete()
    messages.success(request, 'Account deleted')
    return redirect('/dashboard/selling_accounts')



def trade_requests_all(request):
    trade_requests = Trade_Requests.objects.filter(Q(Q(trade_account__owner=request.user) & Q(approved=True)) | Q(account_owner=request.user)).all()
    return render(request, 'dashboard/trade_requests.html', {
        "trade_requests": trade_requests,
    })


def decline_trade(request, trade_id):
    trade = Trade_Requests.objects.get(pk=trade_id)
    trade.answer = False
    trade.completed = True
    trade.save()

    return redirect('/dashboard/trade_requests_all')


def accept_trade(request, trade_id):

    trade = Trade_Requests.objects.get(pk=trade_id)
    trade.answer = True
    trade.completed = True
    trade.save()

    account = Accounts.objects.get(pk=trade.trade_account.pk)
    account.is_avalabile = False
    account.save()

    current_site = get_current_site(request)

    mail_subject = 'Trade request Accepted'
    message = render_to_string('dashboard/request_accepted.html', {
        'user': trade.account_owner,
        'account': trade.trade_account,
        'domain': current_site,
    })
    to_email = trade.account_owner.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    account = {'email': trade.account_email, 'password': trade.account_password}
    message = render_to_string('dashboard/request_accepted.html', {
        'user': trade.trade_account.owner,
        'domain': current_site,
        'account': account
    })
    to_email = trade.trade_account.owner.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()


    return redirect('/dashboard/trade_requests_all')
