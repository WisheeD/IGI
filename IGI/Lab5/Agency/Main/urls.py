from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', RegisterView, name='register'),

    path('home/', HomeView, name='home'),
    path('list_coupon/', CouponListView, name='list_coupon'),

    path('privacy/', PrivacyView, name='privacy'),
    path('company/', CompanyView, name='company'),

    path('list_news/', NewsView, name='list_news'),
    path('news/<int:pk>/', NewsDetailView, name='news_detail'),

    path('list_question/', QuestionView, name='list_question'),
    path('list_employee/', EmployeeView, name='list_employee'),

    path('list_vacancy/', VacancyView, name='list_vacancy'),
    path('list_vacancy/<int:pk>/', VacancyDetailView, name='vacancy_detail'),

    path('list_review/', ReviewView, name='list_review'),
    path('create_review/', CreateReviewView, name='create_review'),

    path('user_profile/', UserProfileView, name='user_profile'),
    path('employee_profile/', EmployeeProfileView, name='agent_profile'),

    path('age_distribution/', age_distribution_view, name='age_distribution_view'),
    path('age-distribution-chart/', age_distribution_chart, name='age_distribution_chart'),

    path('list_realty/', RealtyView, name='list_realty'),
    path('list_my_realty/', RealtyView, name='list_my_realty'),
    path('realty_create/', RealtyCreateView, name='realty_create'),
    path('edit_realty/<int:pk>/', RealtyUpdateView, name='edit_realty'),
    path('delete_realty/<int:pk>/', RealtyDeleteView, name='delete_realty'),
    path('list_purchased/', PurchasedRealtyView, name='list_purchased'),
    re_path(r'^buy_realty/(?P<pk>\d+)/$', BuyRealtyView, name='buy_realty'),
    re_path(r'^realty/(?P<pk>\d+)/$', RealtyDetailView, name='realty_detail'),

    path('list_deal/', DealView, name='list_deal'),
    path('deal/<int:pk>/', DealDetailView, name='deal_detail'),
    path('deal/<int:pk>/reject/', RejectDealView, name='reject_deal'),
    path('deal/<int:pk>/approve/', ApproveDealView, name='approve_deal'),
]
