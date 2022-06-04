#==>Library Import
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.views import View
import requests
import datetime
import json
#==>Local Import
from .forms import CartAddForm, CouponApplyForm, OrderForm
from .models import Order, OrderItem, Coupon
from account.models import ProfileAddress
from product.models import Variant
from .cart import Cart


class CartView(View):
	def get(self, request):
		cart = Cart(request)
		return render(request, 'orders/cart.html', {'cart':cart})


class CartAddView(View):
	def post(self, request, product_id):
		cart = Cart(request)
		product = Variant.objects.get(id=product_id)
		form = CartAddForm(request.POST)
		if form.is_valid():
			cart.add(product, form.cleaned_data['quantity'])
		messages.success(request, 'محصول مورد نظر به سبد خرید اضافه شد', 'success')
		return redirect('product:detail', product.slug)


class CartRemoveView(View):
	def get(self, request, product_id):
		cart = Cart(request)
		product = get_object_or_404(Variant, id=product_id)
		cart.remove(product)
		messages.success(request, 'محصول مورد نظر از سبد خرید حذف شد', 'warning')
		return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
	form_class = CouponApplyForm

	def get(self, request, order_id):
		order_form = OrderForm(instance=request.user.profile)
		order = get_object_or_404(Order, id=order_id)
		user_address = ProfileAddress.objects.filter(user_id=request.user.id)
		return render(request, 'orders/order.html', {'order':order, 'form':self.form_class, 'order_form':order_form, 'user_address':user_address})

	def post(self, request, order_id):
		order_form = OrderForm(request.POST, instance=request.user.profile)
		if order_form.is_valid():
			new_order = order_form.save(commit=False)
			new_order.user = request.user
			new_order.save()
			order_address = get_object_or_404(Order, id=order_id)
			order_address.address = order_form.cleaned_data['address']
			order_address.save()
			return redirect('orders:order_detail', order_id)


class OrderCreateView(LoginRequiredMixin, View):
	def get(self, request):
		cart = Cart(request)
		order = Order.objects.create(user=request.user)
		for item in cart:
			OrderItem.objects.create(order=order, variant=item['product'], price=item['total_price'], quantity=item['quantity'])
		cart.clear()
		return redirect('orders:order_detail', order.id)


MERCHANT = settings.MERCHANT
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/order/verify/'

class OrderPayView(LoginRequiredMixin, View):
	def get(self, request, order_id):
		order = Order.objects.get(id=order_id)
		request.session['order_pay'] = {
			'order_id': order.id,
		}
		req_data = {
			"merchant_id": MERCHANT,
			"amount": order.get_total_price(),
			"callback_url": CallbackURL,
			"description": description,
			"metadata": {"mobile": request.user.phone, "email": request.user.email}
		}
		req_header = {"accept": "application/json",
					  "content-type": "application/json'"}
		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
			req_data), headers=req_header)
		authority = req.json()['data']['authority']
		if len(req.json()['errors']) == 0:
			return redirect(ZP_API_STARTPAY.format(authority=authority))
		else:
			e_code = req.json()['errors']['code']
			e_message = req.json()['errors']['message']
			return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
	def get(self, request):
		order_id = request.session['order_pay']['order_id']
		order = Order.objects.get(id=int(order_id))
		t_status = request.GET.get('Status')
		t_authority = request.GET['Authority']
		if request.GET.get('Status') == 'OK':
			req_header = {"accept": "application/json",
						  "content-type": "application/json'"}
			req_data = {
				"merchant_id": MERCHANT,
				"amount": order.get_total_price(),
				"authority": t_authority
			}
			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
			if len(req.json()['errors']) == 0:
				t_status = req.json()['data']['code']
				if t_status == 100:
					order.paid = True
					order.orderitem_order.sell += 1
					order.save()
					return HttpResponse('Transaction success.\nRefID: ' + str(
						req.json()['data']['ref_id']
					))
				elif t_status == 101:
					return HttpResponse('Transaction submitted : ' + str(
						req.json()['data']['message']
					))
				else:
					return HttpResponse('Transaction failed.\nStatus: ' + str(
						req.json()['data']['message']
					))
			else:
				e_code = req.json()['errors']['code']
				e_message = req.json()['errors']['message']
				return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
		else:
			return HttpResponse('Transaction failed or canceled by user')


class CouponApplyView(LoginRequiredMixin, View):
	form_class = CouponApplyForm

	def post(self, request, order_id):
		now = datetime.datetime.now()
		form = self.form_class(request.POST)
		if form.is_valid():
			code = form.cleaned_data['code']
			try:
				coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
			except Coupon.DoesNotExist:
				messages.error(request, 'this coupon does not exists', 'danger')
				return redirect('orders:order_detail', order_id)
			order = Order.objects.get(id=order_id)
			order.discount = coupon.discount
			order.save()
			messages.success(request, "کوپن اعمال شد", 'success')
		return redirect('orders:order_detail', order_id)