# Generated by Django 4.2.2 on 2023-07-05 20:23

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_shopcategory_delete_snipcartsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='shop.shopcategory'),
        ),
    ]