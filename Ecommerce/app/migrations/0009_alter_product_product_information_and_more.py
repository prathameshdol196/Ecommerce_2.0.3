# Generated by Django 4.2.4 on 2023-08-27 10:14

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Product_Information',
            field=ckeditor.fields.RichTextField(null=True),
        ),
        migrations.AlterModelTable(
            name='product',
            table='app_Product',
        ),
    ]
