from django.contrib import admin
from .models import User 

@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','username','phone_number','is_email_verified')
    search_fields = ('email','username','phone_number')
