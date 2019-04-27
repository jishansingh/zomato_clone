from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('logout/',views.logout_user,name='logout'),
    path('send/', views.send_request,name='send_request'),
    path('show/', views.show,name='show'),
    path('order/delivery/', views.order_delivery,name='order_delivery'),
    path('approve/<id>/', views.approve,name='approve'),
    path('cart/', views.cart,name='cart'),
    path('delivered/<pk>/', views.delivered,name='delivered'),
    path('login/', views.customer_login,name='customer_login'),
    path('valet/login/', views.valet_login,name='valet_login'),
    path('valet/register/', views.valet_register,name='valet_register'),
    path('order/<pk>/', views.order_food,name='order_food'),
    path('order/<id>/<pk>/', views.order_food,name='order_food'),
    path('profile/', views.profile,name='profile'),
    path('edit_menu/<id>/', views.edit_menu,name='edit_menu'),
    path('edit/', views.edit_profile,name='edit_profile'),#list_restraunt
    path('addcart/<id>/<pk>/<state>/<city>/', views.add_to_cart,name='add_to_cart'),
    path('list/', views.list_restraunt,name='list_restraunt'),
    path('list/<id>/', views.list_restraunt,name='list_restraunt'),
    path('add/',views.add_restraunt,name='add_restraunt'),
    path('create/',views.ProfileCreate,name='ProfileCreate'),
    path('<state>/', views.restraunt_all,name='restraunt_all'),
    path('<state>/<city>/', views.restraunt_city,name='restraunt_city'),
    path('<state>/<city>/<id>/', views.restraunt_detail,name='restraunt_detail'),
    
]
