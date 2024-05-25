from django.utils import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    city = models.CharField(max_length=100, verbose_name='Город')
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Страна')
    timezone = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    work = models.TextField(blank=True, null=True, verbose_name='Выполняемые работы')
    image = models.ImageField(blank=True, null=True, verbose_name='Аватар', upload_to='user_images/')

    def __str__(self):
        return self.username


class News(models.Model):
    content = models.TextField(verbose_name='Содержание')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    summary = models.TextField(max_length=500, verbose_name='Краткое содержание')
    date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение', blank=True, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    question = models.TextField(max_length=1000, verbose_name='Вопрос')
    answer = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Ответ')

    def __str__(self):
        return self.question


class Review(models.Model):
    grade = models.CharField(max_length=1, verbose_name='Оценка')
    review = models.TextField(max_length=1000, verbose_name='Отзыв')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    author = models.CharField(max_length=255, null=True, verbose_name='Автор')


class Realty(models.Model):
    class Meta:
        verbose_name = 'Realty'
        verbose_name_plural = 'Realties'

    def __str__(self):
        return self.name

    STATUS_CHOICES = (
        ('available', 'Доступно'),
        ('sold', 'Продано'),
        ('unavailable', 'Недоступно'),
    )

    area = models.IntegerField(verbose_name='Площадь')
    name = models.CharField(max_length=100, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    realty_type = models.CharField(max_length=20, verbose_name='Тип')
    description = models.TextField(max_length=1000, verbose_name="Описание")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Стоимость')
    discount = models.DecimalField(default=0, decimal_places=2, max_digits=10, verbose_name='Скидка')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение', upload_to='realty_images/')
    agent = models.ManyToManyField(User, related_name='assigned_properties', blank=True, verbose_name='Агент')


class Coupon(models.Model):
    description = models.TextField(verbose_name='Описание')
    code = models.CharField(max_length=50, verbose_name='Промокод')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    date_created = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    discount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Скидка')
    date_expired = models.DateTimeField(blank=True, null=True, verbose_name='Дата истечения срока')

    def __str__(self):
        return self.code


class Vacancy(models.Model):
    description = models.TextField(verbose_name='Описание')
    title = models.CharField(max_length=255, verbose_name='Название')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    def __str__(self):
        return self.title


class Deal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]

    date = models.DateTimeField(default=timezone.now, verbose_name='Дата сделки')
    amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Сумма сделки')
    property = models.ForeignKey(Realty, on_delete=models.CASCADE, verbose_name='Недвижимость')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_deals', verbose_name='Клиент')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус сделки')
    deal_type = models.CharField(max_length=20, choices=[('sale', 'Sale'), ('rent', 'Rent')], verbose_name='Тип сделки')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_deals', null=True, verbose_name='Агент')

    def __str__(self):
        return f'{self.property.name} - {self.client.username} - {self.agent.username}'


class Company(models.Model):
    requisites = models.TextField(verbose_name='Реквизиты')
    description = models.TextField(verbose_name='Описание')
    history = models.TextField(verbose_name='История компании')
    name = models.CharField(max_length=100, verbose_name='Название')
    logo = models.ImageField(upload_to='company_logos/', verbose_name='Логотип')
    video_filename = models.CharField(max_length=100, verbose_name='Имя файла видео', blank=True)

    def __str__(self):
        return self.name
