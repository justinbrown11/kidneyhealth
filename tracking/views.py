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