#==>Library Import
from django.contrib import admin
#==>Local Import
from .models import Product, Category, Variant, Color, Size, Comment


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created',)


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variant)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Comment)
