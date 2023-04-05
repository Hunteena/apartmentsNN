# Generated by Django 4.1.7 on 2023-04-04 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flats', '0004_alter_apartment_options_alter_comfort_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главная страница',
            },
        ),
        migrations.RemoveField(
            model_name='image',
            name='apartment',
        ),
        migrations.CreateModel(
            name='MainPageSliderImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flats.image')),
                ('slider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slider_images', to='flats.mainpage')),
            ],
            bases=('flats.image',),
        ),
        migrations.CreateModel(
            name='ApartmentImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flats.image')),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='flats.apartment')),
            ],
            bases=('flats.image',),
        ),
    ]
