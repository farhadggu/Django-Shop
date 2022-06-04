#==>Library Import
from django.contrib import admin
#==>Local Import
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ('variant',)
	readonly_fields = ('variant', 'price', 'quantity')
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'updated', 'paid', 'get_total_price')
	list_filter = ('paid',)
	readonly_fields = ('paid', 'address', 'get_total_price')
	inlines = (OrderItemInline,)


admin.site.register(Coupon)