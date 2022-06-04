# Generated by Django 4.0.4 on 2022-06-03 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_color_options_alter_size_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='visit_count',
        ),
        migrations.AddField(
            model_name='variant',
            name='available',
            field=models.BooleanField(default=True, verbose_name='موجود؟'),
        ),
        migrations.AddField(
            model_name='variant',
            name='visit_count',
            field=models.ManyToManyField(blank=True, related_name='visit_count', to='product.ipaddress', verbose_name='بازدید'),
        ),
    ]
