from django.contrib import admin
from .models import Restraunt,Review,Menu,UserProfile
# Register your models here.
admin.site.register(Restraunt)
admin.site.register(Review)
admin.site.register(Menu)
admin.site.register(UserProfile)