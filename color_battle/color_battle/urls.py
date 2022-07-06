from django.contrib import admin
from django.urls import path, include
from back_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('back_api.urls')),
    path('', views.index, name='index')
]
