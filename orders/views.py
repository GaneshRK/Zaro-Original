from decimal import Decimal
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.conf import settings

import razorpay

from courses.models import Course
from .models import Order, PromoCode


razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

@login_required
def checkout(request):
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request")

    course_ids = request.POST.getlist('courses')
    promo_code_value = request.POST.get('promo_code')

    courses = Course.objects.filter(id__in=course_ids)

    if not courses.exists():
        return HttpResponseBadRequest("No courses selected")

    # Original amount = sum of discount_price of selected courses
    total_amount = sum(course.discount_price for course in courses)

    # Get promo code object if exists (no discount logic)
    promo_code = None
    if promo_code_value:
        try:
            promo_code = PromoCode.objects.get(code__iexact=promo_code_value, is_active=True)
        except PromoCode.DoesNotExist:
            promo_code = None

    # Create Order
    order = Order.objects.create(
        user=request.user,
        original_amount=total_amount,
        discount_amount=0,  # no discount from promo
        total_amount=total_amount,
        promo_code=promo_code,
        status='pending'
    )

    order.courses.add(*courses)

    # Razorpay order
    razorpay_order = razorpay_client.order.create({
        'amount': int(total_amount * 100),  # in paise
        'currency': 'INR',
        'payment_capture': 1
    })

    order.razorpay_order_id = razorpay_order['id']
    order.save()

    context = {
        'order': razorpay_order,
        'order_obj': order,
        'courses': courses,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'total_amount': total_amount
    }

    return render(request, 'orders/checkout.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            order = Order.objects.get(razorpay_order_id=order_id)

            # VERIFY SIGNATURE
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.status = 'paid'
            order.save()

            return redirect('/')

        except Exception:
            return HttpResponseBadRequest("Payment verification failed")

    return HttpResponseBadRequest("Invalid request")
