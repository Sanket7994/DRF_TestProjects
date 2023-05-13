from django.contrib import admin
from django.urls import path, include

# Functions


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
]
