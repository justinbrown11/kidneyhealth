from django.urls import path
from .views import dailyPageView, indexPageView, weeklyPageView, monthlyPageView, searchResultsPageView


urlpatterns = [
    path('daily/', dailyPageView, name = 'daily'),
    path('weekly/', weeklyPageView, name = 'weekly'),
    path('monthly/', monthlyPageView, name = 'monthly'),
    path('food/search/', searchResultsPageView, name = 'searchFoodQuery'),
    path('', indexPageView, name = 'index'),
]