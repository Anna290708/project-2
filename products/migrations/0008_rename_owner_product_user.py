# Generated by Django 5.1.2 on 2025-03-15 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='owner',
            new_name='user',
        ),
    ]
