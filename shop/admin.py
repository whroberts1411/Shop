from django.contrib import admin
from .models import Product, Order, Item, Shopper
from django.db import models

#------------------------------------------------------------------------------

# Main Heading for all the admin pages
admin.site.site_header = 'E-Commerce Site'
# Text for the browser page tab
admin.site.site_title = 'Orinoco Online Store'
# Heading for the index page (list of groups, users and models)
admin.site.index_title = 'Administer the Orinoco Online Store'

#------------------------------------------------------------------------------
class ProductAdmin(admin.ModelAdmin):
    """ Change the default behaviour of the admin screen when displaying
        the Item database contents. This also demonstrates how to add our
        own actions to the Action list (by default, only has Delete). """

    def change_category_to_default(self, request, queryset):
        """ Add a new action to change the category to "Default" for the
            selected records in the list. """
        queryset.update(category='Default')

    change_category_to_default.short_description = 'Default Category'

    list_display = ('title', 'category', 'discount_price','description')
    ordering = ('title', 'category')
    search_fields = ('title', 'category', 'description')
    actions = ('change_category_to_default',)
    # Only display these fields on the "Change" screen
    fields = ('title','price','discount_price','category','description','image')
    # Allow these fields to be edited on the list screen
    list_editable = ('category', 'discount_price')
    # Limit the number of items shown on each page
    list_per_page = 5

#------------------------------------------------------------------------------
class OrderAdmin(admin.ModelAdmin):

    list_display = ('orderdate',)
    ordering = ('orderdate',)
    search_fields = ('orderdate',)

#------------------------------------------------------------------------------
class ShopperAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'postcode')
    ordering = ('name', 'postcode')
    search_fields = ('name', 'postcode', 'city')

#------------------------------------------------------------------------------
class ItemAdmin(admin.ModelAdmin):

    list_display = ('item', 'order', 'cost')
    ordering = ('item',)
    search_fields = ('item', 'cost', 'quantity', 'order')
    list_per_page = 15

#------------------------------------------------------------------------------
""" This must be actioned after any class definitions, and must also register
    the class definitions. """

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Shopper, ShopperAdmin)
admin.site.register(Item, ItemAdmin)

#------------------------------------------------------------------------------
