from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Lab, Food
from .forms import LabForm, ExtendedUserCreationForm, ProfileForm
import requests
import environ

# Set env
env = environ.Env()

# Import functions
from .functions.searchFood import searchFood

# Create your views here.

def indexPageView(request):
    return render(request, 'tracking/index.html')

def dailyPageView(request):
    return render(request, 'tracking/daily.html')

def searchResultsPageView(request):
    """
    The page view with results from food searching
    """
    try:
        # Grab query param from request
        query = request.GET.__getitem__("query")

        # Search food
        data = searchFood(query)

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

def saveAPIFood(request):

    try:
        # Grab query param from request
        food = request.GET.__getitem__("food")

        # Set body for request
        payload = {
            "api_key": env('FOOD_API_KEY'),
            "nutrients": "203,305,306,307"
        }

        # Send request
        outcome = (requests.get(f"{env('FOOD_API_URL')}/food/{food}", params=payload)).json()

        newFood = {}

        # If food is branded
        if (outcome['dataType'] == 'Branded'):

            protien = 0.00
            phosphorus = 0.00
            potassium = 0.00
            sodium = 0.00

            # Loop through nutrients
            for nutrient in outcome['foodNutrients']:
                if (nutrient['nutrient']['name'] == 'Protein'):
                    protien = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Phosphorus, P'):
                    phosphorus = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Potassium, K'):
                    potassium = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Sodium, Na'):
                    sodium = float(nutrient['amount'])

            print(protien,phosphorus,potassium,sodium)

            # Add new food        
            newFood = Food(
                food_description=outcome['description'], 
                brand_name=outcome['brandName'], 
                serving_size=float(outcome['servingSize']), 
                serving_size_unit=outcome['servingSizeUnit'],
                protien_g=protien,
                phosphorus_mg=phosphorus,
                potassium_mg=potassium,
                sodium_mg=sodium
            )

        else:
            protien = 0.00
            phosphorus = 0.00
            potassium = 0.00
            sodium = 0.00

            # Loop through nutrients
            for nutrient in outcome['foodNutrients']:
                if (nutrient['nutrient']['name'] == 'Protein'):
                    protien = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Phosphorus, P'):
                    phosphorus = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Potassium, K'):
                    potassium = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Sodium, Na'):
                    sodium = float(nutrient['amount'])

            # Add new food        
            newFood = Food(
                food_description=outcome['description'], 
                protien_g=protien,
                phosphorus_mg=phosphorus,
                potassium_mg=potassium,
                sodium_mg=sodium
            )
        
        # Save new food
        newFood.save()

        return redirect('/search')
            
    except Exception as e:
        # Log error
        print(e)

        # Render error page
        return render(request, 'tracking/error.html')


def saveCustomFood(request):

    try:
        # Grab body from request
        body = dict(request.POST.items())

        print(body)

        # Add new food        
        newFood = Food(
            food_description=body['food_description'], 
            brand_name=body['brand_name'] if body['brand_name'] else None, 
            serving_size=float(body['serving_size']) if body['serving_size'] else None, 
            serving_size_unit=body['serving_size_unit'] if body['serving_size_unit'] else None,
            protien_g=body['protien_g'],
            phosphorus_mg=body['phosphorus_mg'],
            potassium_mg=body['potassium_mg'],
            sodium_mg=body['sodium_mg']
        )
        
        # Save new food
        newFood.save()

        return redirect('/customFood')
            
    except Exception as e:
        # Log error
        print(e)

        # Render error page
        return render(request, 'tracking/error.html')


def weeklyPageView(request):
    return render(request, 'tracking/weekly.html')

def monthlyPageView(request):
    return render(request, 'tracking/monthly.html')

def accountCreationPageView(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data('username')
            password = form.cleaned_data('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
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

def customFoodPageView(request):
    return render(request, 'tracking/customFood.html')