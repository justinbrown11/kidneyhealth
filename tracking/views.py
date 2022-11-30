from django.shortcuts import render, redirect
from .models import Lab
from .forms import LabForm

# Import functions
from .functions.searchFood import searchFood

# Create your views here.

def indexPageView(request):
    return render(request, 'tracking/index.html')

def dailyPageView(request):
    return render(request, 'tracking/daily.html')

async def searchResultsPageView(request):
    """
    The page view with results from food searching
    """
    try:
        # Grab query param from request
        query = request.GET.__getitem__("query")

        # Search food
        data = await searchFood(query)

        # Check for error
        if (data['result'] == 1):
            raise Exception("Error occured searching food")

        # Set context
        context = {
            "foods": data['data']['foods']
        }

        return render(request, 'tracking/searchResults.html', context)

    except Exception as e:
        # Log error
        print(e)

        # Render error page
        return render(request, 'tracking/error.html')

def weeklyPageView(request):
    return render(request, 'tracking/weekly.html')

def monthlyPageView(request):
    return render(request, 'tracking/monthly.html')

def loginPageView(request):
    return render(request, 'tracking/login.html')

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

def viewLabsPageView(request):
    data = Lab.objects.all()
    if request.method == 'POST':
        form = LabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/viewLabs')
    else:
        form = LabForm()
    context = {
        'data': data,
        'form': form,
    }

    return render(request, 'tracking/viewLabs.html', context)

def addLabsPageView(request):
    return render(request, 'tracking/addLabs.html')

def errorPageView(request):
    return render(request, 'tracking/error.html')

def tipsPageView(request):
    return render(request, 'tracking/tips.html')