from django.db import models


class Apartment(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
        help_text='Введите название апартаментов'
    )
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
        help_text='Введите заголовок для части описания апартаментов'
    )
    address = models.CharField(
        max_length=512,
        verbose_name='Адрес',
        help_text='Введите адрес апартаментов'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание апартаментов'
    )
    # images ForeignKey
    shortCharacteristic = models.CharField(
        max_length=512,
        verbose_name='Короткое описание',
        help_text='Введите короткое описание через запятую для отображения под названием апартаментов'
    )
    # detailedCharacteristic ForeignKey
    # comfort ForeignKey
    # location OneToOneField
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        help_text='Введите цену апартаментов'
    )
    capacity = models.PositiveSmallIntegerField(
        verbose_name='Максимальная вместительность',
        help_text='Введите максимальную вместительность'
    )

    def __str__(self):
        return f"{self.name} ({self.shortCharacteristic})"

    class Meta:
        verbose_name = 'Апартаменты'
        verbose_name_plural = 'Список апартаментов'


class Image(models.Model):
    photo = models.ImageField(
        upload_to='photos/',
        verbose_name='Фотография',
        help_text='Выберите файл с изображением'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
        help_text='Введите название фотографии'
    )
    altName = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name='Альтернативное название',
        help_text='Введите альтернативное название'
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Список фотографий'



class DetailedCharacteristic(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='Название',
        help_text='Введите название характеристики'
    )
    data = models.CharField(
        max_length=512,
        verbose_name='Значение',
        help_text='Введите значение характеристики'
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='detailedCharacteristic'
    )

    def __str__(self):
        return f"{self.name}: {self.data}"

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Список характеристик'


class Comfort(models.Model):
    type = models.CharField(
        max_length=128,
        verbose_name='Тип',
        help_text='Введите тип опции комфорт'
    )
    description = models.CharField(
        max_length=512,
        verbose_name='Описание',
        help_text='Введите описание опции комфорт'
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='comfort'
    )

    def __str__(self):
        return f"{self.type}: {self.description}"

    class Meta:
        verbose_name = 'Опция комфорт'
        verbose_name_plural = 'Список опций комфорт'


class Location(models.Model):
    url = models.URLField(
        verbose_name='Ссылка на карты',
        help_text='Введите ссылку на карты'
    )
    desc = models.CharField(
        max_length=512,
        verbose_name='Описание',
        help_text='Введите описание расположения через запятую для отображением под заголовком расположения'
    )
    apartment = models.OneToOneField(
        Apartment,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name = 'Расположение'
        verbose_name_plural = 'Список расположений'

