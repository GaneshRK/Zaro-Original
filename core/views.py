from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from courses.models import Course
from .models import ContactMessage


def home(request):
    elite_courses = Course.objects.filter(category='elite')
    premium_courses = Course.objects.filter(category='premium')

    context = {
        'elite_courses': elite_courses,
        'premium_courses': premium_courses,
    }

    return render(request, 'home/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('core:contact')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        # Send email to admin
        send_mail(
            subject=f"New Contact Message from {name}",
            message=(
                f"New message received on ZARO website.\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                f"Message:\n{message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully.")
        return redirect('core:contact')

    return render(request, 'supports/contact.html')


def privacy_policy(request):
    return render(request, 'supports/privacy.html')


def terms_conditions(request):
    return render(request, 'supports/terms.html')
