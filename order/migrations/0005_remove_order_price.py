# Generated by Django 4.0.4 on 2022-05-30 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
    ]