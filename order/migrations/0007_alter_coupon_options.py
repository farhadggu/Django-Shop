# Generated by Django 4.0.4 on 2022-06-03 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_order_options_alter_orderitem_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'کد تخفیف', 'verbose_name_plural': 'کد های تخفیف'},
        ),
    ]