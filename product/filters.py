# Standard library import
import django_filters
from django import forms
# Local import
from .models import Color, Size, Variant


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Variant
        fields = [
            'color',
            'size',
            'sell',
            'discount'
        ]
    CHOICE1 = {
        ('گران ترین', 'گران ترین'),
        ('ارزان ترین', 'ارزان ترین'),
    }

    CHOICE2 = {
        ('پرفروش ترین', 'پرفروش ترین'),
        ('کم قروش ترین', 'کم قروش ترین')
    }

    CHOICE3 = {
        ('بیشترین تخفیف', 'بیشترین تخفیف'),
        ('کمترین تخفیف', 'کمترین تخفیف')
    }

    price = django_filters.ChoiceFilter(choices=CHOICE1, method='price_filter')
    sell = django_filters.ChoiceFilter(choices=CHOICE2, method='sell_filter')
    discount = django_filters.ChoiceFilter(choices=CHOICE3, method='discount_filter')

    def price_filter(self, queryset, name, value):
        data = 'price' if value == 'ارزان ترین' else '-price'
        return queryset.order_by(data)

    def sell_filter(self, queryset, name, value):
        data = 'sell' if value == 'lowest sell' else '-sell'
        return queryset.order_by(data)

    def discount_filter(self, queryset, name, value):
        data = 'discount' if value == 'کمترین تخفیف' else '-discount'
        return queryset.order_by(data)