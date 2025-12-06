from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from board.models import Ad, Feedback
from front.forms import LoginForm, ResetRequestFrom
from front.utils import api_get, api_post


# Main Page

class MainPageView(View):
    template_name = 'main_page/main_page.html'

    def get(self, request):
        context = {
            'count_ads': Ad.objects.all().count(),
            'count_feedback': Feedback.objects.all().count()
        }
        return render(request, self.template_name, context)


# Ads

def get_ad_list(request):
    url = request.build_absolute_uri(reverse("board:ad_list"))
    data = api_get(url)
    return render(request, 'ad/ad_list.html', {'ads': data})


def ad_create(request):
    token = request.session.get('access')

    if request.method == "POST":
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')

        url = request.build_absolute_uri(reverse("board:ad_create"))
        api_post(
            url,
            {
                'title': title,
                'price': price,
                'description': description
            },
            token
        )

        return redirect('ad_list')

    return render(request, 'ad/ad_create.html')


def ad_detail(request, pk):
    token = request.session.get("access")
    url = request.build_absolute_uri(reverse("ad_detail", args=[pk]))
    data = api_get(url, token)
    return render(request, "ad_detail.html", {"ad": data})


# Feedback

# Users

def user_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)

                token_url = request.build_absolute_uri(reverse("users:login"))
                tokens = api_post(token_url, data={
                    'email': email,
                    'password': password
                })

                request.session['access'] = tokens['access']
                request.session['refresh'] = tokens['refresh']

                return redirect('front:main_page')

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('front:main_page')


def reset_request(request):
    form = ResetRequestFrom()

    if request.method == 'POST':
        form = ResetRequestFrom(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']

            url = request.build_absolute_uri(reverse("users:password-reset-request"))

            api_post(url, data={'email': email})

            return redirect('front:main_page')

    return render(request, 'users/reset_request.html', {'form': form})
