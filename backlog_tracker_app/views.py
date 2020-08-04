from django.shortcuts import render
from django.http import HttpResponse
from backlog_tracker_app.forms import UserForm
from backlog_tracker_app.forms import UserProfileForm
from backlog_tracker_app.models import *

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import json
from demjson import decode

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
                        'Some of the information was not valid.'
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

    #TODO: Remove this
    episodes = requests.get('http://api.tvmaze.com/shows/{}/episodes'.format(show_id))
    episodes = episodes.json()

    return render(request, 'show.html', context={'search_result': search_result, 'episodes': episodes})

@login_required
def update_account(request): 
    if request.method == "POST": 
        new_password = request.POST.get('password')
        new_confirm_password = request.POST.get('confirm-password')

        if new_password == new_confirm_password: 
            current_user = request.user 

            current_user.set_password(new_password) 
            current_user.save()

            return render(request, 'user/update-account.html', context={'success_message': 'You have successfully changed your password'})
        else: 
            return render(request, 'user/update-account.html', context ={
                    'errors': [
                        'The passwords do not match.'
                    ]
                })

    return render(request, 'user/update-account.html', context={})

def backlog(request): 
    shows = ShowBacklog.objects.filter(user=request.user)

    return render(request, 'user/backlog.html', context={'shows': shows})

@login_required
def add_backlog(request, show_id=1): 
    if request.method == "POST": 
        #TODO: remove these api calls if possible
        show = requests.get('http://api.tvmaze.com/shows/{}?embed=episodes'.format(show_id))
        show = show.json() # convert to readable json format

        episodes = requests.get('http://api.tvmaze.com/shows/{}/episodes'.format(show_id))
        episodes = episodes.json()

        #add to database
        ShowBacklog.objects.create(name=show['name'], genre=show['genres'], summary=show['summary'], 
            release_date=show['premiered'], image_url=show['image']['medium'], 
                max_episodes=len(episodes), user=request.user)

        return HttpResponseRedirect(reverse('backlog_tracker_app:show', args=[show_id]))
    
    return HttpResponseRedirect(reverse('backlog_tracker_app:show', args=[show_id]))

@login_required
def update_backlog(request, show_id=1): 
    if request.method == "POST": 
        current_episode = request.POST.get('current-episode')
        updating_show = ShowBacklog.objects.get(user=request.user, id=show_id)

        updating_show.current_episode = current_episode
        updating_show.save() 

        messages.success(request, "You have updated your progress with {} successfully".format(updating_show.name))

        return HttpResponseRedirect(reverse('backlog_tracker_app:backlog'))
        
    return HttpResponseRedirect(reverse('backlog_tracker_app:backlog'))

@login_required
def remove_backlog(request, show_id=1): 
    if request.method == "POST": 
        removing_show = ShowBacklog.objects.get(user=request.user, id=show_id)

        messages.success(request, "You have removed {} from your backlog successfully".format(removing_show.name))

        removing_show.delete() 

        return HttpResponseRedirect(reverse('backlog_tracker_app:backlog'))
        
    return HttpResponseRedirect(reverse('backlog_tracker_app:backlog'))
