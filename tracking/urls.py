from django.urls import path
from .views import dailyPageView, indexPageView, weeklyPageView, monthlyPageView


urlpatterns = [
    path('daily/', dailyPageView, name= 'daily'),
    path('weekly/', weeklyPageView, name= 'weekly'),
    path('monthly/', monthlyPageView, name= 'monthly'),
    path('', indexPageView, name= 'index')
]