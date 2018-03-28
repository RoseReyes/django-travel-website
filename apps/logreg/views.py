from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import User, Travel, UserManager
import bcrypt
# Create your views here.

def index(request):
    return render(request, 'logreg/index.html')

def registration(request):
    response = User.objects.validate_register(request.POST)
    if response['status'] == True:
       request.session['user_id'] = response['user_id']
       return redirect('/travellanding_page')
    else: 
        for error in response['errors']:
            messages.error(request, error, extra_tags="registerError")
        return redirect('/')

def login(request):
        result = User.objects.validate_login(request.POST)
        if type(result) == list:
            for item in result:
                messages.error(request, item, extra_tags="loginError")
            return redirect('/')
        request.session['user_id'] = result.id
        messages.success(request, 'Successfully logged in!')
        return redirect('/travellanding_page')

def travellanding_page(request):
    # display fdata rom all routes should go here #
    if 'user_id' not in request.session:
        return redirect('/')
        
    active_user = User.objects.get(id=request.session['user_id'])

    context = {
        'user': active_user,
        'my_travels': Travel.objects.filter(created_by = active_user),
        'joined_travels':Travel.objects.filter(favorite_user = active_user),
        'all_travels': Travel.objects.exclude(created_by=active_user).exclude(favorite_user = active_user)
    }
    return render(request,'logreg/quotes.html', context)


def addlanding_page(request):
    return render(request,"logreg/addtrip.html")

def addTravel(request):
    
    active_user = User.objects.get(id=request.session['user_id'])
    error =[]
    isValid = False

    if len(request.POST['destination']) < 1 or len(request.POST['description']) < 1:
        error.append("Destination and Description is required")
    if len(request.POST['travel-date-from']) < 1:
        error.append("Travel date from is required")
    if len(request.POST['travel-date-to']) < 1:
        error.append("Travel date to is required")
        for item in error:
            messages.error(request, item, extra_tags ="travelError")
            return redirect('/addlanding_page')
            isvalid = True

    Travel.objects.create(destination = request.POST['destination'], description = request.POST['description'], travel_date_from = request.POST['travel-date-from'], travel_date_to = request.POST['travel-date-to'], created_by = active_user )
    return redirect('/travellanding_page')

def createMyTravels(request):
    request.session['travelID'] = request.POST['travel_id']
    active_user = request.session['user_id']
    add_favorite = User.objects.get(id=active_user).join_travels.add(Travel.objects.get(id=request.session['travelID']))
    return redirect('/travellanding_page')

def destination(request, id):
    travel = Travel.objects.get(id=id)

    context = {
        "joined_user": User.objects.filter(join_travels = travel.id).exclude(id=travel.created_by.id),
        "all_travels": Travel.objects.filter(id=id),
        "user": User.objects.get(id=request.session['user_id'])
    }
    print context
    return render(request,"logreg/users.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')






