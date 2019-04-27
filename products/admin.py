from django.contrib import admin
from .models import UserProfile,Restraunt,Review,Menu,new_request,Delivery,order_detail
# Register your models here.
admin.site.register(Restraunt)
admin.site.register(Review)
admin.site.register(Menu)
admin.site.register(UserProfile)
admin.site.register(new_request)
admin.site.register(Delivery)
admin.site.register(order_detail)