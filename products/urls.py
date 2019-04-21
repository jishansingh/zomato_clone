from django.urls import path

from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('add/',views.add_restraunt,name='add_restraunt'),
    path('create/',views.ProfileCreate,name='ProfileCreate'),
    path('<state>/', views.restraunt_all,name='restraunt_all'),
    path('<state>/<city>/', views.restraunt_city,name='restraunt_city'),
    path('<state>/<city>/<id>/', views.restraunt_detail,name='restraunt_detail'),
    
]
