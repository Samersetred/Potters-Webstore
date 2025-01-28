from django.urls import path
# from .views import home_page_view
from .views import store
from .views import cart
from .views import checkout
from .views import registerPage
from .views import loginPage
from .views import logoutUser
from .views import updateItem

urlpatterns = [
#    path("", home_page_view),
    path("", store, name="store"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path('register/', registerPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('update_item/', updateItem, name="update_item"),
]