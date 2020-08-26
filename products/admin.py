
from django.contrib import admin
from .models import Category, Product,Tag


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','description','price','created')
    search_fields = ('title','description')

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
