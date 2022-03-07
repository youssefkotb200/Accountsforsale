from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from app.models import Categories
from django.core.paginator import Paginator
from cart.models import CartItem, Cart
from cart.views import get_session
from django.db.models import Q
from User_Accounts.models import User
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.


def averageReview(seller_id):
    seller = User.objects.get(pk=seller_id)
    reviews = Review.objects.filter(seller_id=seller).aggregate(average=Avg('stars_review'))
    avg = 0
    if reviews['average'] is not None:
        avg = float(reviews['average'])
    return avg

def account(request, acc_id):
    if request.method == 'GET':
        account = Accounts.objects.filter(is_avalabile=True, pk=acc_id, approved=True).all()
        category = Categories.objects.get(slug=account[0].category.slug)
        equivalent = Accounts.objects.filter(is_avalabile=True, category=category, approved=True).all()[:8]
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(Q(account_id=account[0]) & Q(user_id=request.user)).exists()
        else:
            in_cart = CartItem.objects.filter(Q(account_id=account[0]) & Q(cart_id__cart_id=get_session(request))).exists()
        return render(request, "accounts/account.html", {
            "account": account,
            "equivalent_games": equivalent,
            'In_cart': in_cart,
            'rating': averageReview(account[0].owner.id)
        })


Sort_by_par = ''
KeyWord_main = ''

def accounts(request, option):
    if option[0:2] == 'to':
        accounts = Accounts.objects.filter(is_avalabile=True, price__lte=int(option[2:len(option)]), approved=True).all()
    else:
        accounts = Accounts.objects.filter(is_avalabile=True, approved=True).all()
    accounts_count = accounts.count()
    accounts = sort_by(request, accounts)
    return render(request, "accounts/accounts.html", {
        'Accounts': accounts,
        'Items_found': accounts_count,
        'page_obj': pagination(request.GET.get('page'), accounts),
    })

def account_categories(request, slug_name):
    category = get_object_or_404(Categories, slug=slug_name)
    accounts = Accounts.objects.filter(is_avalabile=True, category=category, approved=True).all()
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
    accounts = Accounts.objects.filter(Q(is_avalabile=True) & Q(Q(title__icontains=KeyWord_main) | Q(category__name__icontains=KeyWord_main)), approved=True).all()
    accounts_count = accounts.count()
    accounts = sort_by(request, accounts)
    return render(request, "accounts/accounts.html", {
        'Accounts': accounts,
        'Items_found': accounts_count,
        'page_obj': pagination(request.GET.get('page'), accounts),
        'keyword': KeyWord_main,
    })


def pagination(page_number, accounts):
    paginator = Paginator(accounts, 3)
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



@login_required
def trade_request(request, account_id):
    account_email = request.POST['email']
    account_password = request.POST['password']
    account_title = request.POST['title']
    account_platform = request.POST['platform']

    if request.FILES:
        account_image = request.FILES['image']

    if not account_email:
        messages.error(request, 'all fields is required')
        return redirect('/accounts/account/' + account_id)
    
    if not account_password:
        messages.error(request, 'all fields is required')
        return redirect('/accounts/account/' + account_id)

    if not account_title:
        messages.error(request, 'all fields is required')
        return redirect('/accounts/account/' + account_id)

    if not account_platform:
        messages.error(request, 'all fields is required')
        return redirect('/accounts/account/' + account_id)

    trade_account = Accounts.objects.get(pk=account_id)

    trade_request = Trade_Requests.objects.create(
        account_email=account_email,
        account_password=account_password,
        account_title=account_title,
        account_platform=account_platform,
        trade_account=trade_account,
        account_img=account_image,
        account_owner=request.user
    )

    trade_request.save()

    user = User.objects.get(pk=trade_account.owner.id)

    mail_subject = 'You Recived a Trade Request'
    message = render_to_string('accounts/trade_request_recived.html', {
        'request': request,
        'user': user,
        'trade_account': trade_account,
    })

    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()
    
    messages.success(request, 'Your request have been recived, within two days it will be reviwed.')
    return redirect('/accounts/account/' + account_id)