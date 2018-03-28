from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def validate_register(self, postData):
        result ={'status': False
        }
        reg_error = []

        if len(postData['name']) < 1 or len(postData['username']) < 1: 
            reg_error.append('Name and Username is required')
        if len(postData['name']) < 2:
            reg_error.append('Name should be longer than 2 characters')
       
        # check database for duplicate username
        if len(User.objects.filter(username=postData['username'])) > 0:
            reg_error.append("This account is already in use. Log-in or use another username") 
        if len(postData['password']) < 8:
            reg_error.append('Password cannot be less than 8 characters')
        if postData['password'] != postData['cpassword']:
            reg_error.append('Passwords do not match')

        # IF the error list is empty then hashed the password and insert in the database
        if len(reg_error):
            result['errors'] = reg_error
        else:
            # hashed the password then add to the database - salt generation is already included in django's pwd hashing, encode() returns the
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt())
            new_user = User.objects.create(name = postData['name'], username = postData['username'],password = hashed)
            result['status'] = True
            result['user_id'] = new_user.id
        return result

    def validate_login(self, postData):
        error = []
        user = User.objects.filter(username=postData['username'])
        print user
        if len(user) > 0:
            hashed_password = user[0].password
            if not bcrypt.checkpw(postData['password'].encode(), hashed_password.encode()):
                error.append("Username not found")
        else:
            error.append("Username not found")
        if len(error):
            return error
        return user[0]

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    def __repr__(self):
        return "<name: {}, username: {}, created_at: {}".format(self.name, self.username, self.created_at)

class Travel(models.Model):
    created_by = models.ForeignKey(User, related_name = "created_travels") 
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    favorite_user = models.ManyToManyField(User, related_name = "join_travels")
    created_at = models.DateTimeField(auto_now_add=True)
    def __repr__(self):
        return "<created_by: {}, destination: {}, description: {}, travel_date_from: {}, travel_date_to: {}, created_at: {}".format(self.created_by,self.destination, self.description, self.travel_date_from, self.travel_date_to, self.created_at)

