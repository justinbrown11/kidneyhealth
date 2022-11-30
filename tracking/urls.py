from django.urls import path
from tracking.views import dailyPageView, indexPageView, weeklyPageView, monthlyPageView, searchResultsPageView, viewUserInfoPageView, addLabsPageView,accountCreationPageView,deleteUserPageView, errorPageView, searchPageView, updateUserInfoPageView, viewLabsPageView, tipsPageView, saveAPIFood

urlpatterns = [
    path('daily/', dailyPageView, name = 'daily'),
    path('weekly/', weeklyPageView, name = 'weekly'),
    path('monthly/', monthlyPageView, name = 'monthly'),
    path('userInfo/', viewUserInfoPageView, name = 'userInfo'),
    path('addLabs/', addLabsPageView, name = 'addLabs'),
    path('createAccount/', accountCreationPageView, name = 'createAccount'),
    path('deleteUser/', deleteUserPageView, name = 'deleteUser'),
    path('error/', errorPageView, name = 'error'),
    path('search/', searchPageView, name = 'search'),
    path('updateUserInfo/', updateUserInfoPageView, name = 'updateUserInfo'),
    path('viewLabs/', viewLabsPageView, name = 'viewLabs'),
    path('food/search/', searchResultsPageView, name = 'searchFoodQuery'),
    path('tips/', tipsPageView, name = 'tips'),
    path('', indexPageView, name = 'index'),
    path('food/api/save', saveAPIFood, name = 'saveApiFood'),
]