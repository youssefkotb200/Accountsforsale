
from .models import Categories
from cart.models import Cart, CartItem
from cart.views import get_session


def menu_links(request):
    categories_all = Categories.objects.all()
    return dict(categories=categories_all)

def cart_items(request):
    if request.user.is_authenticated:
        cartitems = CartItem.objects.filter(user_id=request.user).all()
    else:
        try:
            cart = Cart.objects.get(cart_id=get_session(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id =  get_session(request),
            )
            cart.save()
        cartitems = CartItem.objects.filter(cart_id=cart).all()
    return dict(cart=cartitems.count())
