#==>Library Import
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.html import format_html
from django.conf import settings
#==>Local Import
from extensions.utils import jalali_converter


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد شده')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ آپدیت شده')

    class Meta:
        abstract = True

    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = 'تاریخ'

    def jupdated(self):
        return jalali_converter(self.updated)


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آی پی آدرس')

    class Meta:
        verbose_name = 'آی پی آدرس'
        verbose_name_plural = 'آی پی آدرس ها'
    
    def __str__(self):
        return self.ip_address


class Category(TimeStamp):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='category_parent', null=True, blank=True, verbose_name='دسته بندی پدر')
    is_sub = models.BooleanField(default=False, verbose_name='دسته  بندی فرزند؟')
    title = models.CharField(max_length=200, verbose_name='نام')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('product:category', args=(self.slug,))


class Product(TimeStamp):
    category = models.ManyToManyField(Category, related_name='product_category', verbose_name='دسته بندی')
    title = models.CharField(max_length=200, verbose_name='نام')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    description = RichTextField(verbose_name='توضیحات')
    

    class Meta:
        ordering = ('-created',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:detail', args=(self.slug,))

    def image_thumbnail(self):
        return format_html('<img src="{}" width=100 />'.format(self.image.url))
    image_thumbnail.short_description = 'تصویر'


class Color(TimeStamp):
    title = models.CharField(max_length=100, verbose_name='نام رنگ')
    code = models.CharField(max_length=100, blank=True, null=True, verbose_name='کد رنگ')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ ها'

    def __str__(self):
        return self.title

    def color_tag(self):
        if self.code is not None:
            return format_html('<p style="background-color:{}" />Color</p>'.format(self.code))
        else:
            return ""


class Size(TimeStamp):
    title = models.CharField(max_length=100, verbose_name='نام سایز')

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز ها'

    def __str__(self):
        return self.title


class Variant(TimeStamp):
    title = models.CharField(max_length=200, verbose_name='نام تنوع')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='اسلاگ')
    image = models.ImageField(verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variant_product', verbose_name='محصول')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True, related_name='variant_color', verbose_name='رنگ')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True, blank=True, related_name='variant_size', verbose_name='سایز')
    quantity = models.IntegerField(default=0, verbose_name='تعداد')
    weight = models.IntegerField(null=True, blank=True, verbose_name='وزن')
    sell = models.IntegerField(default=0, verbose_name='فروش')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    discount = models.IntegerField(verbose_name='تخفیف')
    total_price = models.IntegerField(default=0, null=True, blank=True, verbose_name='قیمت اصلی(تخفیف خورده)')
    visit_count = models.ManyToManyField(IPAddress, blank=True, related_name='visit_count', verbose_name='بازدید')
    available = models.BooleanField(default=True, verbose_name='موجود؟')

    class Meta:
        verbose_name = 'تنوع'
        verbose_name_plural = 'تنوع ها'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.discount:
            self.total_price = self.price
        elif self.discount:
            total = (self.price * self.discount) / 100
            total_price = int(self.price - total)
            self.total_price = total_price
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:detail', args=(self.slug,))


class Comment(TimeStamp):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment_product', verbose_name='محصول')
    body = models.TextField(verbose_name='متن')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user.username} commented {self.body[:10]}'