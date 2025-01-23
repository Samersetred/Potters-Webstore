from django.urls import path
# from .views import home_page_view
from .views import store
from .views import cart
from .views import checkout

urlpatterns = [
#    path("", home_page_view),
    path("", store, name="store"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
]