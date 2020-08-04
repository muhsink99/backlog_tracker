from django.shortcuts import render
from django.http import HttpResponse
from backlog_tracker_app.forms import UserForm
from backlog_tracker_app.forms import UserProfileForm
from backlog_tracker_app.models import *

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import requests
# Create your views here.

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def form(request): 
    return render(request, 'form.html')

def signup(request): 

    signed_up = False 

    if request.method == "POST": 
        user_form = UserForm(data=request.POST)

        if user_form.is_valid(): 

            user = user_form.save() 
            user.set_password(user.password) 
            user.save() 

            signed_up = True 
        else: 
            print(user_form.errors)

    else: 
        user_form = UserForm()

    print(signed_up)

    return render(request, 'user/signup.html', {
        'user_form': user_form, 
        'signed_up': signed_up
    })

def user_login(request): 
    # user is attempting to login... 
    if request.method == 'POST': 
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)

        if user: 
            if user.is_active: 
                login(request, user)
            
                return HttpResponseRedirect(reverse('backlog_tracker_app:index'))
            
            else: 
                return render(request, 'user/login.html', context ={
                    'errors': [
                        'Account is currently not active. Please contact a system admin'
                    ]
                })

        else: 
            print('Someone tried to login and failed! Account does not exist')
            return render(request, 'user/login.html', context ={
                    'errors': [
                        'Account does not exist.'
                    ]
                })

    return render(request, 'user/login.html', context={})

@login_required
def user_logout(request): 
    logout(request) 
    return HttpResponseRedirect(reverse('backlog_tracker_app:index'))

def catalogue(request): 
    if request.method == "POST": 
        search_query = request.POST.get('search-query')
        
        search_results = requests.get('http://api.tvmaze.com/search/shows?q=' + search_query + "&embed=episodes")
        search_results = search_results.json() # convert to readable json format

        return render(request, 'catalogue.html', context={'search_results': search_results})

    return render(request, 'catalogue.html', context={})

def show(request, show_id=0): 
    #TODO: Remove API call
    search_result = requests.get('http://api.tvmaze.com/shows/{}?embed=episodes'.format(show_id))
    search_result = search_result.json() # convert to readable json format

    #TODO: Remove this shit
    episodes = requests.get('http://api.tvmaze.com/shows/{}/episodes'.format(show_id))
    episodes = episodes.json()

    return render(request, 'show.html', context={'search_result': search_result, 'episodes': episodes})

@login_required
def update_account(request): 
    return render(request, 'user/update-account.html', context={})

def backlog(request): 
    return render(request, 'user/backlog.html', context={})

@login_required
def add_backlog(request, show_id=1): 
    if request.method == "POST": 
        show = request.POST.get('show') 
        print(show)

        # add to database
        
        return HttpResponseRedirect(reverse('backlog_tracker_app:show', args=[show_id]))
    
    return HttpResponseRedirect(reverse('backlog_tracker_app:show', args=[show_id]))
