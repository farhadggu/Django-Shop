#==>Library Import
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.db.models import Max, Min
from django.contrib import messages
from django.db.models import Count
from django.views import View
#==>Local Import
from .models import Category, Variant
from order.forms import CartAddForm
from .filters import ProductFilter
from .forms import CommentForm
from order.cart import Cart


class NavbarView(View):
    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        cart = Cart(request)
        return render(request, 'inc/navbar.html', {'categories':categories, 'cart':cart})


class HomeView(View):
    def get(self, request):
        products = Variant.objects.filter(available=True)[:8]
        most_sell_products = Variant.objects.order_by('-sell')[:8]
        most_visited_posts = Variant.objects.annotate(p_count=Count('visit_count')).order_by('-p_count')[:8]
        most_visited_posts = Variant.objects.all()
        categories = Category.objects.filter(is_sub=False)
        context = {
            'products':products, 'most_visited_posts': most_visited_posts,
            'most_sell_products':most_sell_products, 'categories':categories,
        }
        return render(request, 'product/home.html', context)


class ProductCategoryList(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = Variant.objects.filter(product__category=category)
        paginator = Paginator(products, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product/category_list.html', {'products':page_obj, 'category':category})

class ProductDetail(View):
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.product_instance = get_object_or_404(Variant, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request ,*args, **kwargs):
        form = self.form_class
        # Product View Count
        ip_address = request.user.ip_address
        self.product_instance.visit_count.add(ip_address)
        # Product Comments
        comments = self.product_instance.product.comment_product.all()
        cart_form = CartAddForm()
        categories = Category.objects.filter(product_category=self.product_instance.product)
        related_products = Variant.objects.filter(product__category__in=categories)[:8]
        return render(request, 'product/detail.html', {'product':self.product_instance, 'form':form, 'comments':comments, 'cart_form':cart_form, 'related_products':related_products})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.product = self.product_instance.product
            new_comment.save()
            messages.success(request, 'کامنت شما افزوده شد', 'success')
            return redirect('product:detail', kwargs['slug'])


class ProductListView(View):
    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        products = Variant.objects.all()
        filtered_products = ProductFilter(request.GET, queryset=products)
        products = filtered_products.qs
        mx = Variant.objects.aggregate(price=Max('price'))
        max_price = str(mx['price'])
        mn = Variant.objects.aggregate(price=Min('price'))
        min_price = str(mn['price'])
        paginator = Paginator(products, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'product/product_list.html', {'products':page_obj, 'filter':filtered_products, 'max_price':max_price, 'min_price':min_price, 'categories':categories})