from django.contrib import admin
from .models import registration, upload, login_user 

# Register your models here.

admin.site.register(registration)
admin.site.register(upload)
# admin.site.register(login_user)
