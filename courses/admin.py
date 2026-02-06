from django.contrib import admin
from .models import Course, CourseThumbnail, CoursePDF, CourseVideo

class CourseThumbnailInline(admin.TabularInline):
    model = CourseThumbnail
    extra = 1

class CoursePDFInline(admin.TabularInline):
    model = CoursePDF
    extra = 1

class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'original_price', 'discount_price')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'slogan')
    inlines = [CourseThumbnailInline, CoursePDFInline, CourseVideoInline]
