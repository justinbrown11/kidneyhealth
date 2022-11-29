from django.urls import path
from .views import dailyPageView, indexPageView, weeklyPageView, monthlyPageView, searchResultsPageView
from .views import viewUserInfoPageView, addLabsPageView,accountCreationPageView,deleteUserPageView
from .views import errorPageView, loginPageView, searchPageView, updateUserInfoPageView, viewLabsPageView

urlpatterns = [
    path('daily/', dailyPageView, name = 'daily'),
    path('weekly/', weeklyPageView, name = 'weekly'),
    path('monthly/', monthlyPageView, name = 'monthly'),
    path('userInfo/', viewUserInfoPageView, name = 'userInfo'),
    path('addLabs/', addLabsPageView, name = 'addLabs'),
    path('createAccount/', accountCreationPageView, name = 'createAccount'),
    path('deleteUser/', deleteUserPageView, name = 'deleteUser'),
    path('error/', errorPageView, name = 'error'),
    path('login/', loginPageView, name = 'login'),
    path('search/', searchPageView, name = 'search'),
    path('updateUserInfo/', updateUserInfoPageView, name = 'updateUserInfo'),
    path('viewLabs/', viewLabsPageView, name = 'viewLabs'),
    path('food/search/', searchResultsPageView, name = 'searchFoodQuery'),
    path('', indexPageView, name = 'index'),
]