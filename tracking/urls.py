from django.urls import path
from tracking.views import dailyPageView, myPantryPageView, indexPageView, monthlyPageView, searchAPIResultsPageView
from tracking.views import searchFoodResultsPageView, viewUserInfoPageView, register, deleteUser, deleteUserPageView
from tracking.views import errorPageView, searchPageView, updateUserInfoPageView, viewLabsPageView, tipsPageView
from tracking.views import saveAPIFood, customFoodPageView, saveCustomFood, updateWaterLevel, addFoodToEntry
from tracking.views import editFoodHistoryPageView, editFoodHistory, deleteFoodHistory

urlpatterns = [
    path('daily/', dailyPageView, name = 'daily'),
    path('monthly/', monthlyPageView, name = 'monthly'),
    path('userInfo/', viewUserInfoPageView, name = 'userInfo'),
    path('register/', register, name = 'register'),
    path('deleteUser/', deleteUserPageView, name = 'deleteUserView'),
    path('deleteUser/confirm', deleteUser, name = 'deleteUser'),
    path('error/', errorPageView, name = 'error'),
    path('api/search/', searchPageView, name = 'apiSearch'),
    path('updateUserInfo/', updateUserInfoPageView, name = 'updateUserInfo'),
    path('viewLabs/', viewLabsPageView, name = 'viewLabs'),
    path('food/api/search/', searchAPIResultsPageView, name = 'searchAPIFoodQuery'),
    path('tips/', tipsPageView, name = 'tips'),
    path('', indexPageView, name = 'index'),
    path('food/api/save', saveAPIFood, name = 'saveApiFood'),
    path('customFood', customFoodPageView, name = 'customFood'),
    path('food/custom/save', saveCustomFood, name = 'saveCustomFood'),
    path('myPantry/', myPantryPageView, name = 'myPantry'),
    path('water/save', updateWaterLevel, name = 'updateWater'),
    path('food/search/', searchFoodResultsPageView, name = 'searchFoodQuery'),
    path('food/add/', addFoodToEntry, name = 'addFoodEntry'),
    path('food/edit/<int:id>/<str:name>/<str:quantity>', editFoodHistoryPageView, name = 'editFoodHistoryView'),
    path('food/edit/save/', editFoodHistory, name = 'editFoodHistory'),
    path('food/remove/', deleteFoodHistory, name = 'removeFoodHistory'),
]