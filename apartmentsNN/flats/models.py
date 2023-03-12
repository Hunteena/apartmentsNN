from django.db import models


class Apartment(models.Model):
    name = models.CharField(max_length=128)
    title = models.CharField(max_length=256)
    address = models.CharField(max_length=512)
    description = models.TextField()
    # images ForeignKey
    shortCharacteristic = models.CharField(max_length=512)
    # detailedCharacteristic ForeignKey
    # comfort ForeignKey
    # location OneToOneField
    price = models.PositiveIntegerField()
    capacity = models.PositiveSmallIntegerField()


class Image(models.Model):
    photo = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length=128)
    altName = models.CharField(max_length=256)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='images'
    )


class DetailedCharacteristic(models.Model):
    name = models.CharField(max_length=128)
    data = models.CharField(max_length=512)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='detailed'
    )


class Comfort(models.Model):
    type = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    apartment = models.ForeignKey(
        Apartment,
        on_delete=models.CASCADE,
        related_name='comfort'
    )


class Location(models.Model):
    url = models.URLField()
    desc = models.CharField(max_length=512)
    apartment = models.OneToOneField(
        Apartment,
        on_delete=models.CASCADE
    )
