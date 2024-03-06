from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    # Информация о транспортной компании
    name = models.CharField(max_length=100)  # Название компании
    address = models.CharField(max_length=255)  # Адрес компании
    phone = models.CharField(max_length=20)  # Контактный телефон компании
    email = models.EmailField()  # Электронная почта компании


class Bus(models.Model):
    # Информация об автобусе, принадлежащем компании
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Ссылка на компанию
    number = models.CharField(max_length=50)  # Номер автобуса
    model = models.CharField(max_length=100)  # Модель автобуса
    capacity = models.IntegerField()  # Вместимость автобуса


class Stop(models.Model):
    # Информация об остановке
    name = models.CharField(max_length=100)  # Название остановки
    location = models.CharField(max_length=255)  # Местоположение остановки


class Route(models.Model):
    # Маршрут между двумя остановками
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_stop = models.ForeignKey(Stop, related_name='start_stop', on_delete=models.CASCADE)  # Начальная остановка
    end_stop = models.ForeignKey(Stop, related_name='end_stop', on_delete=models.CASCADE)  # Конечная остановка
    duration = models.DurationField()  # Продолжительность поездки


class RouteStop(models.Model):
    # Промежуточные остановки на маршруте
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # Ссылка на маршрут
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)  # Ссылка на остановку
    index = models.IntegerField()  # Порядковый номер остановки на маршруте
    distance = models.DecimalField(max_digits=10, decimal_places=2)  # Километраж от начальной точки


class Schedule(models.Model):
    # Расписание автобусов
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Ссылка на компанию
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)  # Ссылка на автобус
    route = models.ForeignKey(Route, on_delete=models.CASCADE)  # Ссылка на маршрут
    departure_time = models.DateTimeField()  # Время отправления
    arrival_time = models.DateTimeField()  # Время прибытия
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена билета


class Ticket(models.Model):
    # Информация о билете на автобус
    company = models.ForeignKey(Company, on_delete=models.CASCADE)  # Ссылка на компанию
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на пассажира (пользователя)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)  # Ссылка на расписание
    seat_number = models.IntegerField()  # Номер места
    status = models.CharField(max_length=50)  # Статус билета (например, забронирован, куплен, отменен)
    purchase_time = models.DateTimeField()  # Время покупки билета

