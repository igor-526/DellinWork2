from django.db import models
from autos.models import Car
from profile_management.models import NewUser


class Consumption(models.Model):
    datetime = models.DateTimeField(verbose_name="Дата и время записи",
                                    null=False,
                                    blank=False,
                                    auto_now_add=True)
    driver = models.ForeignKey(to=NewUser,
                               verbose_name="Водитель",
                               null=False,
                               blank=False,
                               on_delete=models.CASCADE)
    consumption = models.FloatField(verbose_name="Расход топлива",
                                    null=False,
                                    blank=False)
    odo = models.IntegerField(verbose_name="Пробег за рейс",
                              null=False,
                              blank=False)
    econ = models.FloatField(verbose_name="Экономия топлива",
                             null=False,
                             blank=False)
    burnout = models.IntegerField(verbose_name="Пережог топлива",
                                  null=False,
                                  blank=False)
    car = models.ForeignKey(verbose_name="Транспортное средство",
                            to=Car,
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=False)
