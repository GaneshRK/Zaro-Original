from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls', namespace='courses')), 
    path('users/', include('users.urls', namespace='users')),        
    path('', include('core.urls', namespace='core')),
    path('orders/', include('orders.urls')),

]
