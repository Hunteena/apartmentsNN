# Generated by Django 4.1.7 on 2023-04-25 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0012_remove_location_url_location_latitude_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'ordering': ['id'], 'verbose_name': 'Апартаменты', 'verbose_name_plural': 'Список апартаментов'},
        ),
    ]
