from django.urls import path

from . import views


urlpatterns = [
    path('catalog/', views.IndexView.as_view(), name='index'),




]