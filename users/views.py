from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from courses.models import Course

@login_required
def dashboard(request):
    user = request.user

    paid_orders = Order.objects.filter(
        user=user,
        status='paid'
    )

    purchased_courses = (
        Course.objects
        .filter(orders__in=paid_orders)
        .prefetch_related(
            'thumbnails',
            'pdfs',
            'videos'
        )
        .distinct()
    )

    return render(request, 'auth/dashboard.html', {
        'user': user,
        'courses': purchased_courses,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == 'POST' and 'register' in request.POST:
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Mark user as active & verified immediately
            user.is_active = True
            user.is_email_verified = True
            user.save()

            messages.success(request, 'Account created successfully. You can log in now.')
            return redirect('users:login')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('core:home')


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email verified! You can now log in.')
        return redirect('users:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('users:login')
