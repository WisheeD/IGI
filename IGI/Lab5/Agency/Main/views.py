import uuid
import logging

import geopy
import requests
from io import BytesIO
from matplotlib import pyplot as plt

from django.http import HttpResponseServerError, HttpResponse

from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from timezonefinder import TimezoneFinder

from .forms import SignUpForm, LoginForm, RealtyForm, ReviewForm
from .models import Review, News, Vacancy, Question, Coupon, Realty, Deal, User


logger = logging.getLogger(__name__)


def HomeView(request):
    sort_by = request.GET.get('sort')
    try:
        if sort_by == 'area':
            realties = Realty.objects.filter(status='available').order_by('area')
        elif sort_by == 'name':
            realties = Realty.objects.filter(status='available').order_by('name')
        else:
            realties = Realty.objects.filter(status='available').order_by('price')
    except Exception as e:
        logger.error(f"Error in HomeView: {e}")
        realties = []

    return render(request, 'home.html', {'realties': realties})


def NewsView(request):
    try:
        news = News.objects.all().order_by('-date')
    except Exception as e:
        logger.error(f"Error in NewsView: {e}")
        news = []

    return render(request, 'list_news.html', {'news': news})


def NewsDetailView(request, pk):
    try:
        current_news = get_object_or_404(News, pk=pk)
    except Exception as e:
        logger.error(f"Error in NewsDetailView: {e}")
        current_news = None

    return render(request, 'news_detail.html', {'current_news': current_news})


def QuestionView(request):
    try:
        questions = Question.objects.all()
    except Exception as e:
        logger.error(f"Error in QuestionView: {e}")
        questions = []

    return render(request, 'list_question.html', {'questions': questions})


def EmployeeView(request):
    try:
        employees = User.objects.filter(is_employee=True)
    except Exception as e:
        logger.error(f"Error in EmployeeView: {e}")
        employees = []

    return render(request, 'list_employee.html', {'employees': employees})


def PrivacyView(request):
    try:
        return render(request, 'privacy.html')
    except Exception as e:
        logger.error(f"Error in PrivacyView: {e}")
        return HttpResponseServerError()


def CompanyView(request):
    try:
        return render(request, 'company.html')
    except Exception as e:
        logger.error(f"Error in CompanyView: {e}")
        return HttpResponseServerError()


def VacancyView(request):
    try:
        vacancies = Vacancy.objects.all().order_by('date_posted')
    except Exception as e:
        logger.error(f"Error in VacancyView: {e}")
        vacancies = []

    return render(request, 'list_vacancy.html', {'vacancies': vacancies})


def VacancyDetailView(request, pk):
    try:
        vacancy = get_object_or_404(Vacancy, pk=pk)
    except Exception as e:
        logger.error(f"Error in VacancyDetailView: {e}")
        vacancy = None

    return render(request, 'vacancy_detail.html', {'vacancy': vacancy})


@login_required
def CreateReviewView(request):
    try:
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.author = request.user.username
                review.save()
                return redirect('/app/list_review')
        else:
            form = ReviewForm()
    except Exception as e:
        logger.error(f"Error in CreateReviewView: {e}")
        form = None

    return render(request, 'create_review.html', {'form': form})


def ReviewView(request):
    try:
        reviews = Review.objects.all().order_by('-date')
    except Exception as e:
        logger.error(f"Error in ReviewView: {e}")
        reviews = []

    return render(request, 'list_review.html', {'reviews': reviews})


def RegisterView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            country = form.cleaned_data.get('country')
            city = form.cleaned_data.get('city')
            time = get_timezone_by_location(country, city)
            if timezone:
                user.timezone = time
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})


def LoginView(request):
    try:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/app/home')
        else:
            form = LoginForm()
    except Exception as e:
        logger.error(f"Error in LoginView: {e}")
        form = None

    return render(request, 'login.html', {'form': form})


@login_required
def LogoutView(request):
    try:
        logout(request)
        return redirect('/app/home')
    except Exception as e:
        logger.error(f"Error in LogoutView: {e}")
        return HttpResponseServerError()


@login_required
def EmployeeProfileView(request):
    try:
        timezone.activate(request.user.timezone)
        context = {
            'user_time': timezone.now(),
        }
    except Exception as e:
        logger.error(f"Error in EmployeeProfileView: {e}")
        context = {}

    return render(request, 'employee_profile.html', context)


@login_required
def UserProfileView(request):
    try:
        user_deals = Deal.objects.filter(client=request.user)
        user_ip = request.META.get('REMOTE_ADDR')
        ip_data = None
        if user_ip:
            response = requests.get('https://api.ipify.org?format=json')
            if response.status_code == 200:
                ip_data = response.json()

        timezone.activate(request.user.timezone)

        context = {
            'user_time': timezone.now(),
            'deals': user_deals,
            'ip_data': ip_data
        }

    except Exception as e:
        logger.error(f"Error in UserProfileView: {e}")
        context = {}

    return render(request, 'user_profile.html', context)


def RealtyView(request):
    try:
        user_realty = Realty.objects.filter(owner=request.user)
    except Exception as e:
        logger.error(f"Error in RealtyView: {e}")
        user_realty = []

    return render(request, 'list_realty.html', {'user_realty': user_realty})


def RealtyDetailView(request, pk):
    try:
        current_realty = get_object_or_404(Realty, pk=pk)
    except Exception as e:
        logger.error(f"Error in RealtyDetailView: {e}")
        current_realty = None

    return render(request, 'realty_detail.html', {'realty': current_realty})


@login_required
def RealtyCreateView(request):
    try:
        if request.method == 'POST':
            form = RealtyForm(request.POST, request.FILES)
            if form.is_valid():
                if request.user.is_authenticated:
                    realty = form.save(commit=False)
                    realty.owner = request.user
                    response = requests.get('https://dog.ceo/api/breeds/image/random')
                    if response.status_code == 200:
                        data = response.json()
                        image_url = data.get('message')
                        if image_url:
                            unique_filename = str(uuid.uuid4())
                            with open(f'media/realty_images/{unique_filename}.jpg', 'wb') as file:
                                file.write(requests.get(image_url).content)
                            realty.image = f'realty_images/{unique_filename}.jpg'
                        realty.save()
                        return redirect('/app/home')
                else:
                    form.add_error(None, "Пользователь не аутентифицирован.")
        else:
            form = RealtyForm()
    except Exception as e:
        logger.error(f"Error in RealtyCreateView: {e}")
        form = None

    return render(request, 'realty_create.html', {'form': form})


def RealtyUpdateView(request, pk):
    try:
        realty = get_object_or_404(Realty, pk=pk)
        if request.method == 'POST':
            update_form = RealtyForm(request.POST, request.FILES, instance=realty)
            if update_form.is_valid():
                update_realty = update_form.save(commit=False)
                if 'image' in request.FILES:
                    image = request.FILES['image']
                    unique_filename = str(uuid.uuid4()) + '.jpg'
                    update_realty.image.save(unique_filename, image)
                update_realty.save()
                return redirect('list_realty')
        else:
            update_form = RealtyForm(instance=realty)
    except Exception as e:
        logger.error(f"Error in RealtyUpdateView: {e}")
        update_form = None

    return render(request, 'edit_realty.html', {'update_form': update_form})


@login_required
def RealtyDeleteView(request, pk):
    try:
        realty = get_object_or_404(Realty, pk=pk)
        if request.method == 'POST':
            realty.delete()
            return redirect('list_realty')
    except Exception as e:
        logger.error(f"Error in RealtyDeleteView: {e}")

    return redirect('list_realty')


def DealView(request):
    try:
        active_deals = Deal.objects.filter(status='pending')
    except Exception as e:
        logger.error(f"Error in DealView: {e}")
        active_deals = []

    return render(request, 'list_deal.html', {'available_deals': active_deals})


@login_required
def DealDetailView(request, pk):
    try:
        deal = get_object_or_404(Deal, pk=pk)
    except Exception as e:
        logger.error(f"Error in DealDetailView: {e}")
        deal = None

    return render(request, 'deal_detail.html', {'deal': deal})


def ApproveDealView(request, pk):
    try:
        deal = get_object_or_404(Deal, pk=pk)
        if request.method == 'POST':
            deal.status = 'approved'
            realty = deal.property
            realty.owner = deal.client
            deal.save()
            realty.save()
            return redirect('deal_detail', pk=pk)
    except Exception as e:
        logger.error(f"Error in ApproveDealView: {e}")

    return redirect('deal_detail', pk=pk)


def RejectDealView(request, pk):
    try:
        deal = get_object_or_404(Deal, pk=pk)
        if request.method == 'POST':
            deal.status = 'rejected'
            deal.save()
            return redirect('deal_detail', pk=pk)
    except Exception as e:
        logger.error(f"Error in RejectDealView: {e}")

    return render(request, 'reject_deal.html', {'deal': deal})


@login_required
def CouponListView(request):
    try:
        active_coupons = Coupon.objects.filter(is_active=True, date_expired__gt=timezone.now())
    except Exception as e:
        logger.error(f"Error in CouponListView: {e}")
        active_coupons = []

    return render(request, 'list_coupon.html', {'active_coupons': active_coupons})


@login_required
def BuyRealtyView(request, pk):
    try:
        if request.method == 'POST':
            realty = get_object_or_404(Realty, pk=pk)
            user = request.user
            if realty.owner == user:
                messages.error(request, 'Вы не можете купить свою собственную недвижимость')
                return redirect('realty_detail', pk=pk)

            deal = Deal.objects.create(
                property=realty,
                client=user,
                deal_type='sale',
                amount=realty.price,
                status='pending'
            )

            realty.status = 'sold'
            realty.save()

            return redirect('realty_detail', pk=pk)
    except Exception as e:
        logger.error(f"Error in BuyRealtyView: {e}")
        messages.error(request, 'Произошла ошибка при покупке недвижимости. Пожалуйста,'
                                ' попробуйте еще раз или обратитесь к администратору.')

    return redirect('reality_detail', pk=pk)


@login_required
def PurchasedRealtyView(request):
    try:
        user = request.user
        purchased_properties = Deal.objects.filter(client=user, status='approved').select_related('property')
    except Exception as e:
        logger.error(f"Error in PurchasedRealtyView: {e}")
        purchased_properties = []

    return render(request, 'list_purchased.html', {'purchased_properties': purchased_properties})


def age_distribution_chart(request):
    users = User.objects.all()
    ages = [int(user.birthdate.today().year - user.birthdate.year -
                ((user.birthdate.today().month, user.birthdate.today().day) <
                 (user.birthdate.month, user.birthdate.day))) for user in users if user.birthdate]

    plt.figure(figsize=(10, 6))
    plt.hist(ages, bins=range(min(ages), max(ages) + 1, 1), edgecolor='black')
    plt.title('Age Distribution of Users')
    plt.xlabel('Age')
    plt.ylabel('Number of Users')
    plt.grid(True)
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    return HttpResponse(buffer, content_type='image/png')


def age_distribution_view(request):
    users = User.objects.all()
    ages = [int(user.birthdate.today().year - user.birthdate.year -
                ((user.birthdate.today().month, user.birthdate.today().day) <
                 (user.birthdate.month, user.birthdate.day))) for user in users if user.birthdate]
    avg_ages = sum(ages) // len(ages)
    return render(request, 'age_distribution.html', {'avg_ages': avg_ages})


def logging(request):
    try:
        logger.debug("Это сообщение отладочного уровня")
        logger.info("Это информационное сообщение")
        logger.warning("Это предупреждение")
        logger.error("Это сообщение об ошибке")
        logger.critical("Это критическое сообщение")
    except Exception as e:
        logger.exception("Произошла ошибка: %s", e)


def get_timezone_by_location(country, city):
    geolocator = geopy.geocoders.Nominatim(user_agent="timezone_app")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        if timezone_str:
            return timezone_str
    return None
