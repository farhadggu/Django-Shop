#==>Local Import
from django.contrib.auth.models import AbstractBaseUser
from django.db.models.signals import post_save
from .manager import UserManager
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='ایمیل کاربر',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length=50, unique=True, verbose_name='نام کاربری')
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن کاربر')
    is_active = models.BooleanField(default=True, verbose_name='مجوز ورود به سایت؟')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین سایت؟')
    email_activate = models.BooleanField(default=False, verbose_name=' ایا ایمیل فعال شده ؟')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس')
    code = models.PositiveSmallIntegerField(verbose_name='رمز یکبار مصرف')
    created = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد شده')

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کد های یکبار مصرف'

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام خانوادگی')
    national_code = models.IntegerField(null=True, blank=True, verbose_name='کد ملی')
    address = models.ForeignKey('ProfileAddress', on_delete=models.CASCADE, null=True, blank=True, related_name='user_address', verbose_name='آدرس')
    image = models.ImageField(null=True, blank=True, verbose_name='عکس')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def __str__(self):
        return f'پروفایل {self.user.username}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class ProfileAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profileaddress_user')
    postal_code = models.IntegerField(null=True, blank=True, verbose_name='کد پستی')
    province = models.CharField(max_length=100, null=True, blank=True, verbose_name='استان')
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name='شهر')
    address = models.TextField(null=True, blank=True, verbose_name='آدرس')

    class Meta:
        verbose_name = 'آدرس کاربر'
        verbose_name_plural = 'آدرس کاربران'

    def __str__(self):
        return f'{self.province} - {self.city} - {self.address}'


def user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(user_profile, sender=User)