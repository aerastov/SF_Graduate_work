from django.db import models
from django.contrib.auth.models import User



class Technique_model(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'


class Engine_model(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателей'


class Transmission_model(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссий'


class Drive_axle_model(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущих мостов'


class Steerable_axle_model(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемых мостов'


class Service_company(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Сервисные компании'
        verbose_name_plural = 'Сервисные компании'

class Car(models.Model):
    factory_number = models.TextField(max_length=17, unique=True, verbose_name='Заводской номер')
    technique_model = models.ForeignKey(Technique_model, on_delete=models.CASCADE)
    engine_model = models.ForeignKey(Engine_model, on_delete=models.CASCADE)
    engine_number = models.TextField(max_length=17, verbose_name='Номер двигателя')
    transmission_model = models.ForeignKey(Transmission_model, on_delete=models.CASCADE)
    transmission_number = models.TextField(max_length=50, verbose_name='Номер трансмиссии')
    drive_axle_model = models.ForeignKey(Drive_axle_model, on_delete=models.CASCADE)
    drive_axle_number = models.TextField(max_length=50, verbose_name='Номер ведущего моста')
    steerable_axle_model = models.ForeignKey(Steerable_axle_model, on_delete=models.CASCADE)
    steerable_axle_number = models.TextField(max_length=50, verbose_name='Номер управляемого моста')
    supply_contract = models.TextField(max_length=50, verbose_name='Договор поставки №, дата.')
    date_of_shipment_from_the_factory = models.DateField(verbose_name='Дата отгрузки с завода')
    consignee = models.TextField(max_length=50, verbose_name='Грузополучатель')
    delivery_address = models.TextField(max_length=150, verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(max_length=150, verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент')
    service_company = models.ForeignKey(Service_company, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.factory_number}'

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'



