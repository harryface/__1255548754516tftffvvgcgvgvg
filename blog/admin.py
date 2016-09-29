from django.contrib import admin
#from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'page']
    list_filter = ['name', 'page']

#admin.site.register(Product, ProductAdmin)
