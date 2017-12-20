from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        name = post['name']
        alias = post['alias']
        email = post['email'].lower()
        password = post['password']
        cpassword = post['cpassword']
        birthday = post['birthday']

        errors=[]

        if len(name)<1 or len(alias)<1 or len(email)<1 or len(password)<1 or len(cpassword)<1 or len(birthday)<1 :
            errors.append("all fields are required")
        else:
            if not EMAIL_REGEX.match(email):
                errors.append("invalid email")
            else:
                if len(User.manager.filter(email=email)) > 0 :
                    errors.append('email is already used')

            if not name.isalpha() or not alias.isalpha():
                errors.append("name and alias: characters only")

            if len(password) < 3 :
                errors.append('password: at least 8 characters')
            elif password != cpassword:
                errors.append('password is not match with comfirm password, please try again')

            if len(birthday) < 1 :
                errors.append("Birthday can not be empty")
            else:
                date_object = datetime.strptime(birthday, '%Y-%m-%d')
                if date_object > datetime.now():
                    errors.append("Birthday should not be future date")
            
        if not errors:
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=name,
                alias=alias,
                email=email,
                password=hashed,
                birthday=birthday,
            )
            return new_user                

        return errors

    def login_validator(self, post):
        email = post['email'].lower()
        password = post['password']

        try:
            user = User.manager.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

    def create_new_user(self, name):
		self.create(name=name)
        
    def add_friend(self, friend_id, user_id):
		me = self.get(id=user_id)
		friend = self.get(id=friend_id)
		me.friends.add(friend)

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    friends = models.ManyToManyField('self')
    manager = UserManager()
