from django.urls import path
from . import views

urlpatterns = [
     path('success/', views.success, name='success'),
     path('', views.HomePageView.as_view(), name='home'),
]