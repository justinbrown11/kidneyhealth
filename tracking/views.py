from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Lab, Food, DailyEntry, Profile, FoodHistory
from .forms import LabForm, ExtendedUserCreationForm, ProfileForm
import requests
import environ
from datetime import date
from json import dumps

# Set env
env = environ.Env()

# Create your views here.

def indexPageView(request):
    return render(request, 'tracking/index.html')

def dailyPageView(request):

    try:

        # Intialize foods array
        foods = []

        # Grab today's entry for the user
        today = (DailyEntry.objects.filter(entry_date=date.today(), user__id=request.user.id)).values()

        # If entry doesn't exist, create one
        if (len(today) < 1):

        # Grab current user
            currentUser = User.objects.get(id=request.user.id)

            # Add new entry
            newEntry = DailyEntry(user=currentUser, entry_date=date.today(), water_intake_liters=0)
            newEntry.save()

            # Grab today's entry for the user
            today = (DailyEntry.objects.filter(entry_date=date.today(), user__id=request.user.id)).values()[0]

        else:
            today = today[0]

        # Grab food histories
        foodHistory = FoodHistory.objects.filter(entry__id=today['id']).values()

        ProteinTotal = 0
        SodiumTotal = 0
        PhosphorusTotal = 0
        PotassiumTotal = 0

        weight = float(request.user.profile.weight) * 0.453592

        RecommendedProtein = round(.6 * weight, 2)
        RecommendedSodium = 2300
        RecommendedPhosphorus = 1000
        RecommendedPotassium = 3000
        RecommendedWater = 2.70

        if request.user.profile.gender.gender_description == "f":
            RecommendedWater = 2.7
        else :
            RecommendedWater = 3.7

        for item in foodHistory:
            food = Food.objects.get(id=item['food_id'])

            ProteinTotal += round(float(food.protein_g * item['quantity']), 2)
            SodiumTotal += float(food.sodium_mg * item['quantity'])
            PhosphorusTotal += float(food.phosphorus_mg * item['quantity'])
            PotassiumTotal += float(food.potassium_mg * item['quantity'])

            # Initialize food dict
            foodDict = {}

            # Update attributes
            foodDict['id'] = item['id']
            foodDict['food_description'] = food.food_description
            foodDict['brand_name'] = food.brand_name
            foodDict['quantity'] = float(item['quantity'])
            foodDict['protein'] = round(float(food.protein_g * item['quantity']), 2)
            foodDict['sodium'] = float(food.sodium_mg * item['quantity'])
            foodDict['phosphorus'] = float(food.phosphorus_mg * item['quantity'])
            foodDict['potassium'] = float(food.potassium_mg * item['quantity'])

            # Push to array
            foods.append(foodDict)

        WaterPercentage = (float(float(today['water_intake_liters'])/RecommendedWater)) * 100
        SodiumPercentage = (float(SodiumTotal/RecommendedSodium)) * 100
        ProteinPercentage = (float(ProteinTotal/RecommendedProtein)) * 100
        PotassiumPercentage = (float(PotassiumTotal/RecommendedPotassium)) * 100
        PhosphorusPercentage = (float(PhosphorusTotal/RecommendedPhosphorus)) * 100

        context = {
            "currentWaterLevel": float(today['water_intake_liters']),
            "currentWaterPercentage": WaterPercentage,
            "currentProteinLevel": ProteinTotal,
            "currentProteinPercentage": ProteinPercentage,
            "currentSodiumLevel": SodiumTotal,
            "currentSodiumPercentage": SodiumPercentage,
            "currentPotassiumLevel": PotassiumTotal,
            "currentPotassiumPercentage": PotassiumPercentage,
            "currentPhosphorusLevel": PhosphorusTotal,
            "currentPhosphorusPercentage": PhosphorusPercentage,
            "recommendedProtein": RecommendedProtein,
            "recommendedSodium": RecommendedSodium,
            "recommendedWater": RecommendedWater,
            "recommendedPhosphorus": RecommendedPhosphorus,
            "recommendedPotassium": RecommendedPotassium,
            "foods": foods
        }

        return render(request, 'tracking/daily.html', context)
    
    except Exception as e:

        # log error
        print(e)

        if (type(e) == User.profile.RelatedObjectDoesNotExist):
            return HttpResponse("<script>alert('User does not have a profile, please create one and try again.'); window.location.href='/logout'</script>")

        else:
            return HttpResponse("<script>alert('An error occured, please login again'); window.location.href='/logout'</script>")


def updateWaterLevel(request):

    try:

        # Grab body from request
        body = dict(request.POST.items())

        # Grab today's entry for the user
        today = DailyEntry.objects.filter(entry_date=date.today(), user__id=request.user.id)[0]

        # If entry exists, update it
        if (today):

            # Update water level
            today.water_intake_liters = float(body['water'])
            today.save()

        # No entry exists, create one
        else:
            # Grab current user
            currentUser = User.objects.get(id=request.user.id)

            # Add new entry
            newEntry = DailyEntry(user=currentUser, entry_date=date.today(), water_intake_liters=float(body['water']))
            newEntry.save()


        return HttpResponse("<script>alert('Water level updated successfully!'); window.location.href='/daily'</script>")


    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to update water intake'); window.location.href='/daily'</script>")


def searchAPIResultsPageView(request):
    """
    The page view with results from food searching
    """
    try:
        # Grab query param from request
        query = request.GET.__getitem__("query")

        # Set body for request
        payload = { 
            "query": query,
            "api_key": env('FOOD_API_KEY')
        }

        # Send request
        data = (requests.get(f"{env('FOOD_API_URL')}/foods/search", params=payload)).json()

        # Set context
        context = {
            "foods": data['foods']
        }

        return render(request, 'tracking/foodApiSearchResults.html', context)

    except Exception as e:
        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to load results, try again'); window.location.href='/api/search'</script>")



def searchFoodResultsPageView(request):
    """
    The page view with results from food searching
    """
    try:
        # Grab query param from request
        query = request.GET.__getitem__("query")

        # Grab foods
        foods = Food.objects.filter(food_description__contains=query).distinct('food_description', 'brand_name').values()

        context = {
            "foods": foods
        }

        return render(request, 'tracking/myPantry.html', context)

    except Exception as e:
        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to load results, try again'); window.location.href='/daily'</script>")


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

            protein = 0.00
            phosphorus = 0.00
            potassium = 0.00
            sodium = 0.00

            # Loop through nutrients
            for nutrient in outcome['foodNutrients']:
                if (nutrient['nutrient']['name'] == 'Protein'):
                    protein = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Phosphorus, P'):
                    phosphorus = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Potassium, K'):
                    potassium = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Sodium, Na'):
                    sodium = float(nutrient['amount'])

            # Add new food        
            newFood = Food(
                food_description=outcome['description'].lower(), 
                brand_name=outcome['brandName'].lower(), 
                serving_size=float(outcome['servingSize']), 
                serving_size_unit=outcome['servingSizeUnit'],
                protein_g=protein,
                phosphorus_mg=phosphorus,
                potassium_mg=potassium,
                sodium_mg=sodium
            )

        else:
            protein = 0.00
            phosphorus = 0.00
            potassium = 0.00
            sodium = 0.00

            # Loop through nutrients
            for nutrient in outcome['foodNutrients']:
                if (nutrient['nutrient']['name'] == 'Protein'):
                    protein = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Phosphorus, P'):
                    phosphorus = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Potassium, K'):
                    potassium = float(nutrient['amount'])
                elif (nutrient['nutrient']['name'] == 'Sodium, Na'):
                    sodium = float(nutrient['amount'])

            # Add new food        
            newFood = Food(
                food_description=outcome['description'].lower(), 
                brand_name='', 
                serving_size=0, 
                serving_size_unit='',
                protein_g=protein,
                phosphorus_mg=phosphorus,
                potassium_mg=potassium,
                sodium_mg=sodium
            )
        
        # Save new food
        newFood.save()

        return HttpResponse("<script>alert('Food saved successfully!'); window.location.href='/api/search'</script>")
            
    except Exception as e:
        # Log error
        print(e)

        # Render error page
        return HttpResponse("<script>alert('Failed to save food, try again'); window.location.href='/api/search'</script>")


def saveCustomFood(request):

    try:
        # Grab body from request
        body = dict(request.POST.items())

        # Add new food        
        newFood = Food(
            food_description=body['food_description'].lower(), 
            brand_name=body['brand_name'].lower() if body['brand_name'] != '' else '', 
            serving_size=float(body['serving_size']) if body['serving_size'] != '' else 0, 
            serving_size_unit=body['serving_size_unit'] if body['serving_size_unit'] != '' else '',
            protein_g=body['protein_g'],
            phosphorus_mg=body['phosphorus_mg'],
            potassium_mg=body['potassium_mg'],
            sodium_mg=body['sodium_mg']
        )
        
        # Save new food
        newFood.save()

        return HttpResponse("<script>alert('Food saved successfully!'); window.location.href='/customFood'</script>")
            
    except Exception as e:
        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to save food, try again'); window.location.href='/customFood'</script>")



def addFoodToEntry(request):

    try:

        # Grab body from request
        body = dict(request.POST.items())

        # Grab today's entry for the user
        today = DailyEntry.objects.filter(entry_date=date.today(), user__id=request.user.id)[0]

        # If entry exists, update it
        if (today):
            # Grab food
            food = Food.objects.get(id=body['food'])

            # Create new food history
            newFoodHistory = FoodHistory(entry=today, food=food, quantity=float(body['quantity']))
            newFoodHistory.save()

        # Entry doesn't exist, create one
        else:
            # Grab current user
            currentUser = User.objects.get(id=request.user.id)

            # Add new entry
            newEntry = DailyEntry(user=currentUser, entry_date=date.today(), water_intake_liters=0)
            newEntry.save()

            # Grab food
            food = Food.objects.get(id=body['food'])

            # Create new food history
            newFoodHistory = FoodHistory(entry=newEntry, food=food, quantity=float(body['quantity']))
            newFoodHistory.save()

        return HttpResponse("<script>alert('Food added successfully!'); window.location.href='/daily'</script>")

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to add food, try again'); window.location.href='/daily'</script>")


def weeklyPageView(request):
    return render(request, 'tracking/weekly.html')

def monthlyPageView(request):

    try:

        # Intialize return array
        returnData = []

        # Recommended values
        weight = float(request.user.profile.weight) * 0.453592

        RecommendedProtein = weight * .6
        RecommendedSodium = 2300
        RecommendedPhosphorus = 1000
        RecommendedPotassium = 3000
        RecommendedWater = 0.00

        if request.user.profile.gender.gender_description == "f":
            RecommendedWater = 2.7
        else :
            RecommendedWater = 3.7

        # Grab current user
        currentUser = User.objects.get(id=request.user.id)

        # Grab all daily entries
        allEntries = DailyEntry.objects.filter(user=currentUser).values()

        # Loop through each daily entry
        for entry in allEntries:

            # Grab all food histories
            foodHistories = FoodHistory.objects.filter(entry__id=entry['id']).values()

            # Initialize totals
            ProteinTotal = 0
            SodiumTotal = 0
            PhosphorusTotal = 0
            PotassiumTotal = 0

            for item in foodHistories:
                food = Food.objects.get(id=item['food_id'])

                ProteinTotal += float(food.protein_g * item['quantity'])
                SodiumTotal += float(food.sodium_mg * item['quantity'])
                PhosphorusTotal += float(food.phosphorus_mg * item['quantity'])
                PotassiumTotal += float(food.potassium_mg * item['quantity'])

            # Intialize counter
            counter = 0

            # Update counter with healthy levels for the day
            if (ProteinTotal <= RecommendedProtein):
                counter = counter + 1
            if (SodiumTotal <= RecommendedSodium):
                counter = counter + 1
            if (PhosphorusTotal <= RecommendedPhosphorus):
                counter = counter + 1
            if (PotassiumTotal <= RecommendedPotassium):
                counter = counter + 1
            if (float(entry['water_intake_liters']) <= RecommendedWater):
                counter = counter + 1

            # Push current entry to return data array
            returnData.append({
                "date": entry['entry_date'],
                "healthyCount": counter
            })

        context = {
            "array": returnData
        }

        json = dumps(context, default=str)

        return render(request, 'tracking/monthly.html', { "data": json })

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to load monthly view'); window.location.href='/daily'</script>")

def register(request):

    try:

        if request.method == 'POST':
            form = ExtendedUserCreationForm(request.POST)
            profile_form = ProfileForm(request.POST)

            if form.is_valid() and profile_form.is_valid():
                user = form.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                profile.save()

                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect('/daily')

        else: 
            form = ExtendedUserCreationForm()
            profile_form = ProfileForm()

        context = {'form' : form, 'profile_form' : profile_form}
        return render(request, 'tracking/register.html', context)

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('An error occured, please try again'); window.location.href='/login'</script>")


def viewUserInfoPageView(request):
    return render(request, 'tracking/userInfo.html')

def updateUserInfoPageView(request):

    try:

        if request.method == 'POST':

            # Grab body from request
            body = dict(request.POST.items())

            # Grab today's entry for the user
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user__id=request.user.id)

            user.email = body['email']
            user.first_name = body['first_name']
            user.last_name = body['last_name']
            profile.phone = body['phone']
            profile.weight = float(body['weight'])
            profile.height = float(body['height'])

            user.save()
            profile.save()

            return redirect('/userInfo')

        else:
            return render(request, 'tracking/updateUserInfo.html')

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to update user info, please try again'); window.location.href='/userInfo'</script>")


def deleteUserPageView(request):
    return render(request, 'tracking/deleteUser.html')


def deleteUser(request):

    try:
        # Grab current user
        user = User.objects.get(id=request.user.id)

        # Delete it
        user.delete()

        return HttpResponse("<script>alert('Your account has been deleted successfully. Goodbye!'); window.location.href='/logout'</script>")

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to delete user, please try again'); window.location.href='/userInfo'</script>")


def deleteFoodHistory(request):

    try:

        # Grab body from request
        body = dict(request.POST.items())

        # Grab food history object
        food = FoodHistory.objects.get(id=body['id'])

        # Delete it
        food.delete()

        return HttpResponse("<script>alert('Food removed successfully from today's journal!'); window.location.href='/daily'</script>")

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to remove food, please try again'); window.location.href='/daily'</script>")


def searchPageView(request):
    return render(request, 'tracking/foodApiSearch.html')

def viewLabsPageView(request):

    try:

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

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('An error occurred'); window.location.href='/daily'</script>")


def editFoodHistoryPageView(request, id, name, quantity):

    context = {
        "id": id,
        "name": name,
        "quantity": quantity
    }

    return render(request, 'tracking/editDailyEntry.html', context)


def editFoodHistory(request):

    try:

        # Grab body from request
        body = dict(request.POST.items())

        # Grab food history object
        food = FoodHistory.objects.get(id=body['id'])

        # Update quantity
        food.quantity = body['quantity']

        # save it
        food.save()

        return HttpResponse("<script>alert('Food updated successfully in today's journal!'); window.location.href='/daily'</script>")

    except Exception as e:

        # Log error
        print(e)

        return HttpResponse("<script>alert('Failed to update food, please try again'); window.location.href='/daily'</script>")

def addLabsPageView(request):
    return render(request, 'tracking/addLabs.html')

def errorPageView(request):
    return render(request, 'tracking/error.html')

def tipsPageView(request):
    return render(request, 'tracking/tips.html')

def customFoodPageView(request):
    return render(request, 'tracking/customFood.html')

def myPantryPageView(request):
    return render(request, 'tracking/myPantry.html')
