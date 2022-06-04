#==>Local Import
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
#==>Local Import
from .models import User, Profile, ProfileAddress


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'phone')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'phone', 'is_active', 'is_admin',)


class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'ایمیل کاربری'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'نام کاربری'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'شماره تلفن'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'رمز عبور'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'تایید رمز عبور'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('همچین ایمیلی موجود می باشد')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('همچین نام کاربری موجود می باشد')
        return username

    def clean_confirm_password(self):
        password1 = self.cleaned_data['password']
        password2 = self.cleaned_data['confirm_password']
        if password1 and password2 and password1 != password2:
            raise ValidationError('رمز عبور و تایید رمز عبور باید مثل هم باشند')
        return password2
    

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'کد اعتبار سنجی'}))


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'ایمیل کاربری'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'رمز عبور'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'national_code', 'address', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'نام خانوادگی'})
        self.fields['national_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'کد ملی'})


class ProfileAddressForm(forms.ModelForm):
    class Meta:
        model = ProfileAddress
        fields = ['postal_code', 'province', 'city', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'کد پستی'})
        self.fields['province'].widget.attrs.update({'class': 'form-control', 'placeholder': 'استان'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'شهر'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'آدرس'})