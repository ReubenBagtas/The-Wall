# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

# from django.db import models

# # Create your models here.
# Login and Registration with validations. Validation errors should appear on the page. Logout as well. Password should be at least 8 characters.
# Display the logged user’s created/joined travel plans; also displays other users’ travel plans. Display should be specific per user.
# Ability to join other users’ travel plans. Once the logged user joins, the travel plan record should move to the Trip Schedule tables.
# Display of a particular travel plan which also indicates the list of users who joined that plan.
# Ability to add new travel plans. Validation applies. The newly added travel plan should appear on logged user’s Trip schedule table.
# You must be able to deploy your work to Amazon EC2 and provide the IP address or subdomain/domain name to where your work has been deployed. 
# Please note that Heroku deployment is not honored.
# Submission Requirement: Your code, exported database file, 
# a text file with the IP address or subdomain/domain name for the deployed work and short video demo link.

from django.db import models
import bcrypt, datetime 

class UserManager(models.Manager):
    def register(self, data):
        error = []
        if len(data['name']) <  3:
           error.append('Fields must be at least 8 characters long')
        if len(data['username']) <  3:
           error.append('Fields must be at least 8 characters long')
        if len(data['password']) <  8:
           error.append('password must be 8 characters long') 
        if len(data['confirm']) <  3:
           error.append('password must be 8 characters long') 
        if not data['name'].isalpha():
            error.append('Name must only contain letters')
        #check if username already exits
        try:
            User.objects.get(username=data['username'])
           
            error.append('username is already registered')
        except:
            pass
        #check password length
        if len(data['password'])<8:
            error.append('Password must be at least 8 characters long')
        #check if password and cofirm matches
        if data['password'] != data['confirm']:
            error.append('Password and Password Confirm must match')
        #checking if there are any errors
        if len(error) == 0:
            print('no errors')
            #bcrypt and salt password
            print 'bcrypt and salt password'
            data['password']=bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user = User.objects.create(name=data['name'], username=data['username'], password=data['password'])
            return {'user': user, 'errors': 'none'}
        else:
            return {'user':'none', 'errors': error}
    
    def login(self,data):
       
        error=[]
        try:
            
            user = User.objects.get(username=data['username'])
           
           
            if bcrypt.hashpw(data['password'].encode('utf-8'), user.password.encode('utf-8')) != user.password.encode('UTF-8'):
                  
                error.append('Incorrect password.')
                
        except:
            error.append('Username has not yet been registered')

        if len(error) == 0:
            return {'user': user, 'errors': 'none'}
        else:
            return {'user': 'none', 'errors': error}
    
    
    def tripprocess(self,data):
        error = []
        if len(data['destination']) == 0:
            error.append('Please enter all fields')
        if len(data['plan']) == 0:
            error.append('Please enter all fields')
        if len(data['startdate']) == 0:
            error.append('Please enter all fields')
        if len(data['enddate']) == 0:
            error.append('Please enter all fields')
        if len(data['plan']) == 0:
            error.append('Please enter all fields')
        # today = datetime.datetime.now().date()
        # if data['startdate']) - today < 1:
        #     error.append('Please enter a valid start date')
        # if data['enddate'] - data['startdate'] < 0:
        #     error.append('Please enter valid end date')

        if len(error) == 0:
            TravelPlans.objects.create(name=data['name'], destination=data['destination'], startdate=data['startdate'], enddate=data['enddate'], plan=data['plan'])
            return{'errors':'none'}
        else:
            return{'errors': error}

  
    

        
       

        
        
        

    

        
          
          



class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TravelPlans(models.Model):
    name = models.CharField(max_length=45)
    destination = models.CharField(max_length=45)
    startdate= models.DateField()
    enddate= models.DateField()
    plan = models.TextField()
    users = models.ManyToManyField(User, related_name='travelplans')
    objects = UserManager()

class Join(models.Model):
    plan_id = models.ForeignKey(TravelPlans)
    user_id = models.ForeignKey(User)
    objects = UserManager()


