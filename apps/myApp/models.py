from __future__ import unicode_literals
import bcrypt
from django.db import models

class UserManager(models.Manager):
    def register(self, **kwargs):
        errors = []
        if len(kwargs["first_name"])  < 3 or len(kwargs["user_name"])  < 3:
            errors.append("User name or first name should be at least 3 characters!")

        if User.objects.filter(user_name = kwargs["user_name"]):
            errors.append("User with this username already exists!")

        if len(kwargs["password"]) < 8:
            errors.append("Password should contain more than 8 characters!")

        if kwargs["password"] != kwargs["confirm_password"]:
            errors.append("Password didnt match the confirmation!")

        if len(errors) > 0:
            return (False, errors)
        else:
            hashed = bcrypt.hashpw((kwargs["password"]).encode(), bcrypt.gensalt())
            e = User.objects.create(first_name = kwargs["first_name"], user_name = kwargs["user_name"], password = hashed, date_hired = kwargs["date_hired"])
            e.save()
            print "New object has been successfully saved!"
            return (True, e)

    def login(self, **kwargs):
        try:
            user = User.objects.get(user_name = kwargs["user_name"])
        except:
            return (False, "Invalid Data!")
        if User.objects.get(user_name = kwargs["user_name"]):
            hashed = bcrypt.hashpw((kwargs["password"]).encode(), User.objects.get(user_name = kwargs["user_name"]).password.encode())
            if User.objects.get(user_name = kwargs["user_name"]).password == hashed:
                e = User.objects.get(user_name= kwargs["user_name"])
                return (True, e)
            else:
                return (False, "Password is incorrect!")
        else:
            return (False, "Email is incorrect!")

class ItemManager(models.Manager):
    def add(self, **library):
        if len(library["item_name"]) < 1:
            return (False, "Fill All the Forms!")
        else:
            i = Item.objects.create(name = library["item_name"], user_id = User.objects.get(id=library["request"]["id"]))
            i.save()
        return (True, i)

class WishManager(models.Manager):
    def submit(self, **library):
        w = Wish.objects.create(item_id = Item.objects.get(id=library["request"]["item_id"]), user_id = User.objects.get(id=library["request"]["id"]))
        w.save()
        return (True, w)


class User(models.Model):
    first_name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=45)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = ItemManager()


class Wish(models.Model):
    item_id = models.ForeignKey(Item)
    user_id = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = WishManager()
