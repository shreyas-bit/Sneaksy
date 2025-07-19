"""Admin configuration for the shop application."""
from django.contrib import admin
from django.contrib.admin import AdminSite
from shop.models import Product,Cart,Wishlist,CartItem ,Order,OrderItem

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)






class MyAdminSite(AdminSite):
    site_header = "Shoe Shop Administration"
    site_title = "Shoe Shop Admin"
    index_title = "Welcome to Shoe Shop Admin"

admin_site = MyAdminSite(name='myadmin')
