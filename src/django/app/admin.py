from django.contrib import admin
from .models import Stock, Trader, Comment, Message
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

class TraderInline(admin.StackedInline):
    model = Trader
    can_delete = False
class UserAdmin (BaseUserAdmin):
    inlines = (TraderInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Stock)
admin.site.register(Comment)
admin.site.register(Message)



# Register your models here.
