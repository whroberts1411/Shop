# Generated by Django 3.2 on 2021-05-19 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20210519_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='order_date',
        ),
    ]
