from django.contrib.auth.models import AbstractUser
from django.db import models

from autos.models import Car
from bases.models import Base


class NewUser(AbstractUser):
    base = models.ForeignKey(Base,
                             verbose_name='ОСП',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    bdate = models.DateField(verbose_name='День рождения',
                             null=True,
                             blank=True)
    telegram_id = models.BigIntegerField(verbose_name="ID Telegram",
                                         null=True,
                                         blank=True)
    dellin_service_number = models.IntegerField(verbose_name='Табельный номер',
                                                null=True,
                                                blank=True)
    settings_last_odo = models.IntegerField(verbose_name="Последний пробег",
                                            null=True,
                                            blank=True)
    settings_last_fuel = models.IntegerField(verbose_name="Последний остаток топлива",
                                             null=True,
                                             blank=True)
    setting_last_auto = models.ForeignKey(to=Car,
                                          verbose_name="Последний автомобиль",
                                          null=True,
                                          blank=True,
                                          on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-is_active', 'first_name', 'last_name']

    def __str__(self):
        return self.first_name + ' ' + self.last_name
