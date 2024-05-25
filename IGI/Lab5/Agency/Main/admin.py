from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'is_employee')
    list_filter = ('username', 'email', 'phone', 'is_employee')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'date')
    list_filter = ('question', 'date')
    search_fields = ('question', 'date')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'grade', 'date')
    list_filter = ('review', 'author', 'date', 'grade')
    search_fields = ('review', 'author__username', 'date')


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'price', 'realty_type', 'owner')
    list_filter = ('realty_type', 'price', 'owner')
    search_fields = ('name', 'address', 'description')


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('property', 'client', 'agent', 'deal_type', 'date', 'amount')
    list_filter = ('deal_type', 'date', 'amount')
    search_fields = ('property__name', 'client', 'agent', 'date')


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title', 'summary', 'content')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title', 'description')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'discount', 'is_active', 'date_created', 'date_expired')
    list_filter = ('is_active', 'date_created', 'date_expired')
    search_fields = ('code', 'description')
