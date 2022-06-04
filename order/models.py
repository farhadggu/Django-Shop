#==>Library Import
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models
#==>Local Import
from product.models import Variant
from account.models import ProfileAddress
from product.models import TimeStamp


class Order(TimeStamp):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders', verbose_name='کاربر')
	paid = models.BooleanField(default=False, verbose_name='پرداخت شده؟')
	discount = models.IntegerField(blank=True, null=True, default=None, verbose_name='تخفیف')
	address = models.ForeignKey(ProfileAddress, on_delete=models.CASCADE, null=True, blank=True, verbose_name='آدرس')

	class Meta:
		ordering = ('paid', '-updated')
		verbose_name = 'سفارش'
		verbose_name_plural = 'سفارشات'

	def __str__(self):
		return f'{self.user} - {str(self.id)}'

	
	def get_total_price(self):
		total = sum(item.get_cost() for item in self.orderitem_order.all())
		if self.discount:
			discount_price = (self.discount / 100) * total
			return int(total - discount_price)
		return total
	get_total_price.short_description = 'قیمت تمام شده (تخفیف محصول/کدتخفیف)'


class OrderItem(TimeStamp):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem_order', verbose_name='سفارش')
	variant = models.ForeignKey(Variant, on_delete=models.CASCADE, verbose_name='محصول')
	price = models.IntegerField(verbose_name='قیمت')
	quantity = models.IntegerField(default=1, verbose_name='تعداد')

	class Meta:
		verbose_name = 'محصول ثبت شده'
		verbose_name_plural = 'محصولات ثبت شده'

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price * self.quantity


class Coupon(models.Model):
	code = models.CharField(max_length=30, unique=True)
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
	active = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'کد تخفیف'
		verbose_name_plural = 'کد های تخفیف'

	def __str__(self):
		return self.code