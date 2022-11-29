from django.shortcuts import render

# Create your views here.

def indexPageView(request):
    return render(request,'tracking/index.html')

def dailyPageView(request):
    return render(request,'tracking/daily.html')

def weeklyPageView(request):
    return render(request,'tracking/weekly.html')

def monthlyPageView(request):
    return render(request,'tracking/monthly.html')

def loginPageView(request):
    return render(request,'tracking/login.html')

def accountCreationPageView(request):
    return render(request, 'tracking/createAccount.html')

def viewUserInfoPageView(request):
    return render(request, 'tracking/userInfo.html')

def updateUserInfoPageView(request):
    return render(request, 'tracking/updateUserInfo.html')

def deleteUserPageView(request):
    return render(request, 'tracking/deleteUser.html')

def searchPageView(request):
    return render(request, 'tracking/search.html')

def searchPageView(request):
    return render(request, 'tracking/search.html')

def viewLabsPageView(request):
    return render(request, 'tracking/viewLabs.html')

def addLabsPageView(request):
    return render(request, 'tracking/addLabs.html')