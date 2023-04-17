# Generated by Django 4.1.7 on 2023-04-17 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0008_remove_comfort_description_remove_comfort_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comfort',
            name='option',
            field=models.CharField(choices=[('wi-fi', 'Бесплатный Wi-Fi'), ('parking', 'Бесплатная общественная парковка поблизости'), ('TV', 'Телевизор'), ('appliances', 'Вся необходимая бытовая техника'), ('linens', 'Постельное белье/полотенца'), ('keyless', 'Бесключевой доступ')], default='wi-fi', help_text='Выберите опцию комфорт', max_length=128, verbose_name='Опция комфорт'),
        ),
    ]