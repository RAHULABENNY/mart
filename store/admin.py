from django.contrib import admin
from .models import Product, Category, Banner



@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'is_active')
    list_filter = ('position', 'is_active')