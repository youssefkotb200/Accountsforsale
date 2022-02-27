from django.http.response import HttpResponse
import json
from .models import *
from django.contrib import messages, auth
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from accounts.models import Accounts
from .forms import RegistrationForm
from User_Accounts.models import User
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from cart.views import get_session
# Create your views here.
from cart.models import CartItem, Cart
import requests
# .order_by('-creation_date')[:1]


def index(request):
    if request.method == 'GET':
        accounts = Accounts.objects.filter(is_avalabile=True).all()[:6]
        latest_released =  reversed(accounts)
        cheapest_product = Accounts.objects.filter(is_avalabile=True).all().order_by('price')[:6]
        play_cat = Categories.objects.get(slug="psn")
        playstation = Accounts.objects.filter(is_avalabile=True, category=play_cat).all()
        return render(request, "app/index.html", {
            "trending_acc": accounts,
            "latest_released": latest_released,
            "cheapest_product": cheapest_product,
            "Playstation_bestseller": playstation,
        })


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        if not email:
            messages.error(request, "All fields are required")
            return HttpResponseRedirect(reverse('login_view'))
        password = request.POST["password"]
        if not password:
            messages.error(request, "All fields are required")
            return HttpResponseRedirect(reverse('login_view'))
        user = auth.authenticate(email=email, password=password)
        # Check if authentication successful
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=get_session(request))
                cartitems = CartItem.objects.filter(cart_id=cart).all()
            except Cart.DoesNotExist:
                cartitems = None
            if cartitems:
                for i in cartitems:
                    cartitem_2 = CartItem.objects.create(
                        user_id = user,
                        account_id=i.account_id
                    )
                    cartitem_2.save()
                    i.delete()
                cart.delete()
            auth.login(request, user)
            messages.success(request, 'Loged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, "username or password are wrong")
            return HttpResponseRedirect(reverse('login_view'))
    else:
        return render(request, "app/login.html")
    


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,phone_number=phone_number, password=password)
            user.phone_number = phone_number
            user.save()
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('app/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/login?command=verification&email='+email)
    else:
        form = RegistrationForm()
    return render(request, "app/register.html", {
        "form": form,
    })

    

@login_required
def logout_view(request):
    auth.logout(request)
    messages.success(request, "Loged Out")
    return HttpResponseRedirect(reverse("index"))

@login_required
def change_avatar(request, avatar_url):
    user = User.objects.get(pk=request.user.pk)
    user.avatar = 'avatars/' + avatar_url
    user.save()
    return HttpResponseRedirect(reverse("index")) 



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return HttpResponseRedirect(reverse('login_view'))
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if email:
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                 # USER ACTIVATION
                current_site = get_current_site(request)
                mail_subject = 'Reset password'
                message = render_to_string('app/resetpasswordemail.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                return redirect('/login')
            else:
                messages.error(request, "Email Does not exists")
                return HttpResponseRedirect(reverse('forgotpassword'))
        else:
            messages.error(request, "Email Field is required")
            return HttpResponseRedirect(reverse('forgotpassword'))
    return render(request, "app/forgotpassword.html")



def resetpassword(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Password Reset email have sent to you")
        return HttpResponseRedirect(reverse('resetpassword_form'))
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('/login')


def resetpassword_form(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm = request.POST['confirm']

        if not password or not confirm:
            messages.error(request, 'All fiedls is required')
            return redirect('/resetpassword_form')
        
        if password != confirm:
            messages.error(request, 'Confirm Password must equal Password')
            return redirect('/resetpassword_form')
        
        uid = request.session.get('uid')
        user = User.objects.get(pk=uid)
        user.set_password(password)
        user.save()
        messages.success(request, "Password Reset succesfuly")
        return redirect('/login')
        
            
    else:
        return render(request, 'app/resetpassword_form.html')