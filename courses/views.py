from django.shortcuts import render, get_object_or_404
from .models import Course
from orders.models import PromoCode

# Display all courses
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    applied_code = None
    promo_error = None
    final_price = course.original_price  # ← show ORIGINAL price by default

    # Promo code handling
    if request.method == 'POST' and 'apply_promo' in request.POST:
        code = request.POST.get('promo_code', '').strip()

        if code:
            promo = PromoCode.objects.filter(code__iexact=code, is_active=True).first()
            if promo:
                applied_code = promo.code
                final_price = course.discount_price  # ← use discounted price after verification
                # Store in session for checkout
                request.session['promo_code'] = promo.code
                request.session['final_price'] = float(final_price)
            else:
                promo_error = "Invalid or inactive promo code"

    return render(request, 'courses/course_details.html', {
        'course': course,
        'final_price': final_price,
        'applied_code': applied_code,
        'promo_error': promo_error,
    })
    
ELITE_COMBO_PRICES = {
    2: 599,
    3: 899,
    4: 1199,
    5: 1399,
}

PREMIUM_COMBO_PRICES = {
    2: 6000,
    3: 8499,
    4: 10499,
    5: 12000,
}

def combo_offer(request):
    elite_courses = Course.objects.filter(category='elite')
    premium_courses = Course.objects.filter(category='premium')

    selected_courses = []
    final_price = None
    combo_error = None
    category = None

    if request.method == 'POST':
        selected_ids = request.POST.getlist('courses')
        selected_courses = Course.objects.filter(id__in=selected_ids)

        if selected_courses.exists():
            categories = set(selected_courses.values_list('category', flat=True))

            # ❌ Prevent mixing categories
            if len(categories) > 1:
                combo_error = "Please select courses from only one category."
            else:
                category = categories.pop()
                count = selected_courses.count()

                if category == 'elite':
                    final_price = ELITE_COMBO_PRICES.get(count)
                elif category == 'premium':
                    final_price = PREMIUM_COMBO_PRICES.get(count)

                if not final_price:
                    combo_error = "Invalid number of courses selected."

    return render(request, 'courses/combo_offer.html', {
        'elite_courses': elite_courses,
        'premium_courses': premium_courses,
        'selected_courses': selected_courses,
        'final_price': final_price,
        'combo_error': combo_error,
    })
