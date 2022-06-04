#==>Library Import
from django import forms
#==>Local Import
from account.models import Profile


class CartAddForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=9, widget=forms.NumberInput(attrs={'value':'1', 'class':'form-control-sm'}))


class CouponApplyForm(forms.Form):
	code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کوپن'}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_code', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام خانوادگی'})
        self.fields['national_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'کد ملی'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'آدرس'})