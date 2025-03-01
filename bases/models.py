from django.db import models
from autos.models import Car

CONSUMPTION_TIME_CHOICES = (
    (0, 'Летний'),
    (1, 'Зимний'),
)


class City(models.Model):
    name = models.CharField(verbose_name='Наименование',
                            null=False,
                            blank=False)
    consumption_time = models.IntegerField(choices=CONSUMPTION_TIME_CHOICES,
                                           verbose_name="Тип расхода топлива",
                                           null=False,
                                           blank=False,
                                           default=1)

    class Meta:
        verbose_name = 'Город',
        verbose_name_plural = 'Города',
        ordering = ['name']

    def __str__(self):
        return self.name


class Base(models.Model):
    name = models.CharField(verbose_name='Наименование',
                            null=False,
                            blank=False)
    city = models.ForeignKey(City,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             )
    autos = models.ManyToManyField(to=Car,
                                   verbose_name="Автомобили")

    class Meta:
        verbose_name = 'ОСП',
        verbose_name_plural = 'ОСП',
        ordering = ['name']

    def __str__(self):
        return self.name
