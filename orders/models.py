from django.db import models
from django.conf import settings
from courses.models import Course


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    salesman_name = models.CharField(max_length=100)

    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.salesman_name})"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    courses = models.ManyToManyField(
        Course,
        related_name='orders'
    )

    # Pricing
    original_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total before any discounts"
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Final payable amount"
    )

    # Promo code (optional)
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    ordered_at = models.DateTimeField(auto_now_add=True)

    # Razorpay fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
