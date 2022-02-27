from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Payment, Order, OrderProduct
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import Accounts
from accounts.views import pagination
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
    })


@login_required
def order(request, order_number):
    orders = Order.objects.get(user=request.user, is_ordered=True, order_number=order_number)
    orderproducts = OrderProduct.objects.filter(order=orders).all()
    return render(request,"dashboard/order.html", {
        'page_obj': pagination(request.GET.get('page'), orderproducts),

    })