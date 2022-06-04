# Generated by Django 4.0.4 on 2022-05-30 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_otpcode_options_profileaddress_profile'),
        ('order', '0002_orderitem_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='address',
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.profileaddress'),
        ),
    ]