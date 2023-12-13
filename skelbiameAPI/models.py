# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
import hashlib


class Tag(models.Model):
    tag = models.SlugField(max_length=30, primary_key=True)

    class Meta:
        managed = True
        db_table = 'tag'

class Role(models.Model):
    role = models.CharField(max_length=20, primary_key=True)

    class Meta:
        managed = False
        db_table = "role"

class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(hashlib.sha256(password).hexdigest())

        return user

    def get_by_natural_key(self, username):
        try:
            return User.objects.get(username=username)
        except ObjectDoesNotExist:
            return None


class User(AbstractBaseUser):
    username = models.SlugField(db_column='userName', max_length=20, primary_key=True)  # Field name made lowercase.
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=100)

    role = models.ForeignKey(Role, db_column="role", on_delete=models.CASCADE)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'


class Advert(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    uploadtime = models.DateTimeField(db_column='uploadTime')  # Field name made lowercase.
    lastupdatetime = models.DateTimeField(db_column='lastUpdateTime', blank=True,
                                          null=True)  # Field name made lowercase.
    tag = models.ForeignKey(Tag, db_column='tag', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='user', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'advert'


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField()
    advertid = models.ForeignKey(Advert, db_column='advertId', on_delete=models.CASCADE)  # Field name made lowercase.
    user = models.ForeignKey(User, db_column='user', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'comment'


class Rating(models.Model):
    positive = models.IntegerField()
    user = models.ForeignKey(User, db_column='user', on_delete=models.CASCADE)  # Field name made lowercase.
    advertid = models.ForeignKey(Advert, db_column='advertId', on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'rating'
