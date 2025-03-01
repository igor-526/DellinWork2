from django.db import models

DRIVER_LICENCE_CATEGORY_CHOICES = (
    (0, 'B'),
    (1, 'C'),
)


class Car(models.Model):
    name = models.CharField(verbose_name="Наименование",
                            max_length=150,
                            null=False,
                            blank=False,
                            unique=False)
    tank = models.IntegerField(verbose_name="Ёмкость топливного бака",
                               null=False,
                               blank=False)
    consumption_winter = models.FloatField(verbose_name="Расход топлива по зиме",
                                           null=False,
                                           blank=False)
    consumption_summer = models.FloatField(verbose_name="Расход топлива по лету",
                                           null=False,
                                           blank=False)
    driver_license_category = models.IntegerField(choices=DRIVER_LICENCE_CATEGORY_CHOICES,
                                                  default=0,
                                                  null=False,
                                                  blank=False)

    class Meta:
        verbose_name = 'Автомобиль',
        verbose_name_plural = 'Автомобили',
        ordering = ['name']

    def __str__(self):
        return self.name
