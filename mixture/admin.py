from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.

class CartInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display        = ('title', 'slug')
    fields              = [('title', 'slug'), ]


class ProductAdmin(admin.ModelAdmin):
    list_display_links  = ['title', 'id']
    list_display        = ('id','title', 'slug', 'price', 'discount_price', 'created')
    list_editable       = ['price', 'discount_price']
    readonly_fields     = ['created']
    fields              = [( 'title', 'slug', 'price', 'discount_price'), 'created', 'image', ('category', 'hashtag'),]
    list_filter         = ['category', 'created']


class CartAdmin(admin.ModelAdmin):
    list_display        = ('id', 'ordered_date', 'ordered')   
    inlines = [CartInline]


class CartItemAdmin(admin.ModelAdmin):
    list_display        = ('id', 'product', 'count', 'ordered', 'cart')
    list_display_links  = ['cart', 'id']


class HashtagAdmin(admin.ModelAdmin):
    list_display        = ('title', 'slug')
    fields              = [('title', 'slug')]




admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Hashtag, HashtagAdmin)

admin.site.site_header = 'ADmin by me'
