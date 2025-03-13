import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import UserRegisterForm
from .models import OTP, MyUser
from django.core.mail import send_mail


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You've successfully registered your account!")
            return redirect('index')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')

    form = UserRegisterForm()
    return render(request, 'account/user_register.html', {"form": form})


def generate_otp_code():
    random_code = random.randint(100000, 999999)
    return random_code


def user_login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        user = authenticate(request, username=user_email, password=user_password)

        if user:
            if user.is_otp_enabled:
                code = generate_otp_code()
                OTP.objects.create(user=user, code=code)

                send_mail(
                    "Your OTP Code",
                    f"Code: {code}",
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=False,
                )

                return redirect('otp_verify', user_id=user.id)
            else:
                login(request, user)
                messages.success(request, "You've successfully logged in!")
                return redirect('index')
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'account/user_login.html')


def user_logout_view(request):
    logout(request)
    messages.success(request, "You've successfully logged out!")
    return redirect('index')


def otp_verification_view(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == 'POST':
        otp_code = request.POST['otp_code']

        otp = OTP.objects.filter(user=user, if_used=False, code=otp_code).last()

        if otp:
            otp.if_used = True
            otp.save()
            login(request, user)
            messages.success(request, "You've successfully logged in!")
            return redirect('index')

        else:
            messages.error(request, 'Wrong OTP code!')

    return render(request, 'account/otp_verify.html', {'user': user})