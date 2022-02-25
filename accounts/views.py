from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import *
from app.models import Categories
from django.core.paginator import Paginator
from cart.models import CartItem, Cart
from cart.views import get_session
from django.db.models import Q

# Create your views here.


def account(request, acc_id):
    if request.method == 'GET':
        account = Accounts.objects.filter(is_avalabile='true', pk=acc_id).all()
        category = Categories.objects.get(slug=account[0].category.slug)
        equivalent = Accounts.objects.filter(is_avalabile='true', category=category).all()[:8]
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(Q(account_id=account[0]) & Q(user_id=request.user)).exists()
        else:
            in_cart = CartItem.objects.filter(Q(account_id=account[0]) & Q(cart_id__cart_id=get_session(request))).exists()
        return render(request, "accounts/account.html", {
            "account": account,
            "equivalent_games": equivalent,
            'In_cart': in_cart
        })


Sort_by_par = ''
KeyWord_main = ''

def accounts(request, option):
    if option[0:2] == 'to':
        accounts = Accounts.objects.filter(is_avalabile='true', price__lte=int(option[2:len(option)])).all()
    else:
        accounts = Accounts.objects.filter(is_avalabile='true').all()
    accounts_count = accounts.count()
    accounts = sort_by(request, accounts)
    return render(request, "accounts/accounts.html", {
        'Accounts': accounts,
        'Items_found': accounts_count,
        'page_obj': pagination(request.GET.get('page'), accounts),
    })

def account_categories(request, slug_name):
    category = get_object_or_404(Categories, slug=slug_name)
    accounts = Accounts.objects.filter(is_avalabile='true', category=category).all()
    accounts_count = accounts.count()
    accounts = sort_by(request, accounts)
    return render(request, "accounts/accounts.html", {
        'Accounts': accounts,
        'Items_found': accounts_count,
        'page_obj': pagination(request.GET.get('page'), accounts),
    })


def search(request):
    global KeyWord_main
    if 'Keyword' in request.GET:
        keyword = request.GET['Keyword']
        if keyword:
            KeyWord_main = keyword
    accounts = Accounts.objects.filter(Q(is_avalabile='true') & Q(Q(title__icontains=KeyWord_main) | Q(category__name__icontains=KeyWord_main))).all()
    accounts_count = accounts.count()
    accounts = sort_by(request, accounts)
    return render(request, "accounts/accounts.html", {
        'Accounts': accounts,
        'Items_found': accounts_count,
        'page_obj': pagination(request.GET.get('page'), accounts),
        'keyword': KeyWord_main,
    })


def pagination(page_number, accounts):
    paginator = Paginator(accounts, 6)
    page_obj = paginator.get_page(page_number)
    return page_obj


def sort_by(request, accounts):
    global Sort_by_par
    if 'sort' in request.GET:
        Sort_by_par = request.GET.get("sort")
    if Sort_by_par == 'l2h':
        account = accounts.order_by('price')
    elif Sort_by_par == 'h2l':
        account = accounts.order_by('-price')
    else:
        account = accounts.reverse()
    return account

