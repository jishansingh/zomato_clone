from django.urls import path

from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('send/', views.send_request,name='send_request'),
    path('edit/', views.edit_profile,name='edit_profile'),#list_restraunt
    path('list/<id>/', views.list_restraunt,name='list_restraunt'),
    path('add/',views.add_restraunt,name='add_restraunt'),
    path('create/',views.ProfileCreate,name='ProfileCreate'),
    path('<state>/', views.restraunt_all,name='restraunt_all'),
    path('<state>/<city>/', views.restraunt_city,name='restraunt_city'),
    path('<state>/<city>/<id>/', views.restraunt_detail,name='restraunt_detail'),
    
]
