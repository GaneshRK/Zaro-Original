from django.db import models

# Course categories
COURSE_CATEGORIES = (
    ('elite', 'Elite'),
    ('premium', 'Premium'),
)

class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=COURSE_CATEGORIES)
    description = models.TextField()
    what_they_Learn = models.TextField(default="Course learning details will be updated soon.")
    who_this_is_for = models.TextField(default="Everyone, who are at the beginning")
    slogan = models.CharField(max_length=255, blank=True, null=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Multiple thumbnails for a course
class CourseThumbnail(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='thumbnails')
    image = models.ImageField(upload_to='course_thumbnails/')

    def __str__(self):
        return f"{self.course.name} Thumbnail"


# Multiple PDFs for a course
class CoursePDF(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pdfs')
    pdf = models.FileField(upload_to='course_pdfs/')

    def __str__(self):
        return f"{self.course.name} PDF"


# Multiple videos for a course
class CourseVideo(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='course_videos/')

    def __str__(self):
        return f"{self.course.name} Video"
