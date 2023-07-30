# Generated by Django 4.1.7 on 2023-05-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_emailtext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='guests',
        ),
        migrations.AddField(
            model_name='booking',
            name='adults',
            field=models.PositiveSmallIntegerField(default=1, help_text='Введите количество взрослых гостей', verbose_name='Количество взрослых гостей'),
        ),
        migrations.AddField(
            model_name='booking',
            name='children',
            field=models.PositiveSmallIntegerField(default=0, help_text='Введите количество детей', verbose_name='Количество детей'),
        ),
        migrations.AlterField(
            model_name='emailtext',
            name='name',
            field=models.CharField(help_text='Изменение этого поля может привести к сбою при отправке почты!', max_length=20, verbose_name='Название шаблона'),
        ),
        migrations.AlterField(
            model_name='emailtext',
            name='subject',
            field=models.CharField(help_text='Введите тему письма', max_length=200, verbose_name='Тема'),
        ),
    ]