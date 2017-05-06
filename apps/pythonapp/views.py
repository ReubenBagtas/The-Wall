# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.shortcuts import render

# # Create your views here.
from django.shortcuts import render, HttpResponse, redirect
from .models import User, TravelPlans, Join
from django.contrib import messages
#html renders
def index(request):
    
   
    if 'id' not in request.session:
        logout_msg= 'You have been logged out'
        messages.add_message(request, messages.ERROR, logout_msg)


    return render(request, 'pythonapp/index.html')
def travels(request):

    data = {
        'travelplans': TravelPlans.objects.exclude(name = request.session['username']),
        'mytravelplans': TravelPlans.objects.filter(name=request.session['username']),
        'joins': Join.objects.filter(user_id=request.session['id'])
    }
    return render(request, 'pythonapp/travels.html', data)

def addtrip(request):
    return render(request, 'pythonapp/addtrip.html')




#processing routes

def register(request):
    data = {
        'name': request.POST['name'],
        'username': request.POST['username'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
        }
    
    post_data = User.objects.register(data)
    if post_data['errors']== 'none':
        request.session['username'] = post_data['user'].username
        request.session['id'] = post_data['user'].id
        register_success = 'Registration Successful, Please Log in'
        messages.add_message(request, messages.ERROR, register_success)
    else:
        for error in post_data['errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')

    return redirect('/')
def login(request):
    
    data = {
        'username': request.POST['username'],
        'password': request.POST['password']
    }
    post_data = User.objects.login(data)

    if post_data['errors'] == 'none':
       
        request.session['id'] = post_data['user'].id
        request.session['username'] = post_data['user'].username
    else:
        for error in post_data['errors']:
            messages.add_message(request, messages.ERROR, error)
            return redirect('/')

    return redirect('/travels')
def logout(request):
  
    del request.session['id']
    return redirect('/')
def tripprocess(request):
    data={
        'name': request.session['username'],
        'destination': request.POST['destination'],
        'startdate': request.POST['startdate'],
        'enddate': request.POST['enddate'],
        'plan': request.POST['plan'],
    }
    post_data = TravelPlans.objects.tripprocess(data) 

    if post_data['errors'] == 'none':
        return redirect('/travels')
    else:
        for error in post_data['errors']:
            messages.add_message(request, messages_ERROR, error)
            return redirect('/addtrip')
def join(request, plan_id):   
    try: 
        Join.objects.get(travelplans_id_id=plan_id, users_id_id=user_id)
    except:
        Join.objects.create(plan_id_id=plan_id, user_id_id=request.session['id'])
        print Join.objects.all()
    print Join.objects.filter(plan_id=plan_id).values()
    return redirect ('/travels')
def destination(request, plan_id):
    data = {
     'plans': TravelPlans.objects.filter(id=plan_id),
     'joins': Join.objects.filter(plan_id_id=plan_id)   
    }
    return render(request, 'pythonapp/destination.html', data)



    




