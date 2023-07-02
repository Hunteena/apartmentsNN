from django.db import models

from apps.users.models import User


class MainPage(models.Model):

    def __str__(self):
        return 'Главная страница'

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'


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

    rooms = models.PositiveSmallIntegerField(
        verbose_name='Количество комнат',
        help_text='Введите количество комнат'
    )
    store = models.CharField(
        max_length=16,
        verbose_name='Этаж',
        help_text='Введите этаж и этажность здания (например, 1 из 2)'
    )
    area = models.PositiveSmallIntegerField(
        verbose_name='Общая площадь',
        help_text='Введите общую площадь'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год постройки',
        help_text='Введите год постройки'
    )

    # comfort ForeignKey
    # location OneToOneField
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        help_text='Введите цену апартаментов'
    )
    capacity = models.PositiveSmallIntegerField(
        verbose_name='Максимальная вместимость',
        help_text='Введите максимальную вместимость'
    )
    owner = models.ForeignKey(
        User,
        related_name='apartments',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Владелец',
        help_text='Выберите владельца'
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Апартаменты'
        verbose_name_plural = 'Список апартаментов'
        ordering = ['id']


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


class ApartmentImage(Image):
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='images'
    )
    group = models.SmallIntegerField(
        verbose_name='Номер группы',
        help_text='Введите целое число (можно отрицательное), '
                  'которое будет использованно для сортировки групп',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Список фотографий'
        ordering = ['group']


class MainPageSliderImage(Image):
    slider = models.ForeignKey(
        MainPage,
        on_delete=models.CASCADE,
        related_name='slider_images'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Слайдер'


class Comfort(models.Model):

    class ComfortOptions(models.TextChoices):
        wifi = 'wi-fi', 'Бесплатный Wi-Fi'
        parking = 'parking', 'Бесплатная общественная парковка поблизости'
        tv = 'TV', 'Телевизор'
        appliances = 'appliances', 'Вся необходимая бытовая техника'
        linens = 'linens', 'Постельное белье/полотенца'
        key = 'key', 'Бесключевой доступ'
        view = 'view', 'Вид на реку'
        bathhouse = 'bathhouse', 'Сауна (оплачивается отдельно)'
        entrance = 'entrance', 'Отдельный вход'
        tea = 'tea/coffee', 'Чай/кофе'

    option = models.CharField(
        max_length=128,
        choices=ComfortOptions.choices,
        default=ComfortOptions.wifi,
        verbose_name='Опция комфорт',
        help_text='Выберите опцию комфорт'
    )
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='comfort'
    )

    def __str__(self):
        return self.option

    class Meta:
        verbose_name = 'Опция комфорт'
        verbose_name_plural = 'Список опций комфорт'


class Location(models.Model):
    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Введите широту'
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Введите долготу'
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
