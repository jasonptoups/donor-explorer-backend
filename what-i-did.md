# What I Did: Documenting my Process

## Set up Django Settings
I started by setting up Django in the standard way. I made a GitHub repo, cloned it down, cd'd into that. And then in my terminal, I ran the following commands:
```bash
$ virtualenv .env -p python3
$ source .env/bin/activate
# The above code creates a virtual environment called env. 
# You can terminate a virtual environment by running ```$ deactivate```

$ pip install Django===2.0.5
$ pip install psycopg2
$ pip install djangorestframework
$ pip install djangorestframework-simplejwt
$ pip freeze > requirements.txt
# This will save all your installed dependencies to a requirements.txt file

django-admin startproject jinja_test
cd jinja_test
# This will create a django project and move you into that file
```

Now, in a new terminal tab, launch PSQL and set up a database. 
```
$ psql
jasontoups= CREATE DATABASE donor_explorer;
jasontoups= CREATE USER beep WITH PASSWORD 'beepbeep';
jasontoups= GRANT ALL PRIVILEGES ON DATABASE donor_explorer TO beep;
```

In settings.py, tell Django to use your new database and user account:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'donor_explorer',
        'USER': 'beep',
        'PASSWORD': 'beepbeep',
        'HOST': 'localhost'
    }
}
```

At this point, let's also start configuring the Django REST framework with JWTs. In that same settings.py file on the project director (donor-explorer), add the ```REST_FRAMEWORK``` section below. Also edit the ```INSTALLED_APPS``` list to include the rest_framework:
```python
INSTALLED_APPS = [
    'rest_framework'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}
```
I'm taking the above from the djangorestframework-simplejwt documentation at https://github.com/davesque/django-rest-framework-simplejwt and from Django ViewFlow's excellent Medium post at https://medium.com/netscape/full-stack-django-quick-start-with-jwt-auth-and-react-redux-part-i-37853685ab57  

Now let's add a Donors App to our Project. From the project directory of your app, run the following in your terminal:
```bash
$ python manage.py startapp donors
```
This should give you two directories. One is called donor-explorer and is our project directory. The other is called donors and is our app directory. They are on the same level as each other.  

## Set up the JWT API
Let's set up the JWT API. Go to the urls.py file in your project directory:
```python
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', include(
        'rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/obtain', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh', TokenRefreshView.as_view()),
]
```
Now we can test this! In your terminal, run ```$ python manage.py migrate``` and ```$ python manage.py runserver```. Then you can go to http://localhost:8000/api/auth/token/obtain. Enter some credentials and then you should get back an object with a refresh and access token! Yay! 


## Models
Let's go to the app we created (donors in this case) and create our models. In the models.py file:
```python
from django.db import models
from django.contrib.auth.models import User
# Here we're importing the default User class in Django, which we use in SavedDonor as a Foreign Key


class SavedDonor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    employer = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    average_donation = models.IntegerField()
    max_donation = models.IntegerField()
    mode_donation = models.IntegerField()
    total_donations = models.IntegerField()
    user = models.ForeignKey(
          User,
          # to_field='username',
          # If I wanted to show this as the username isntead of the pk, I would add the above line of code
          on_delete=models.CASCADE,
          related_name='donors',
          null=True,
          blank=True
    )

    def __str__(self):
        return self.last_name

    # this method will show us the last name when we just reference the User model
```
The model is pretty standard. The only thing I am doing differently is using the standard User model as a foreign key for Saved Donors. You can see more options on the models at https://docs.djangoproject.com/en/2.0/topics/db/models/. One thing I did is to connect each SavedDonor with a User. In this case, each Saved Donor will only have one User, although each user may have many Saved Donors.  

After setting up the models, we have to register them so we can view them in the admin. Then we migrate and create a super user so we can access the admin panel. Go first to the admin.py file in the app directory:
```python
from django.contrib import admin
from .models import SavedDonor

admin.site.register(SavedDonor)
```
Note that we don't register the User model because by default it already is.  


Then, go to your terminal and run the following commands:
```bash 
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
Now you can test it by going to http://localhost:8000/admin and logging in with the superuser account you created. You should now see your two models and be able to create, edit, and delete. 

## Create Serializers for the Models
Now that we have a model, we want to be able to request it at an api route. Start by defining the route for this api in the project ```donor_explorer/urls.py``` file. 
```python
urlpatterns = [
    ...
    path('api/donors', include('donors.urls'))
]
```

Then, go to the APP directory. Create a serializers.py file. This will turn our model into JSON:
```python
from rest_framework import serializers
from .models import SavedDonor
from django.contrib.auth.models import User

class SavedDonorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # I decided to make this a primaryKeyRelatedField. I could have used a SlugRelatedField instead and it would look like this:
        # user = serializers.SlugRelatedField(read_only=True,
        #                                 many=False,
        #                                 slug_field='username')

    class Meta:
        model = SavedDonor
        fields = ('pk',
                  'first_name',
                  'last_name',
                  'city',
                  'state',
                  'employer',
                  'occupation',
                  'average_donation',
                  'max_donation',
                  'mode_donation',
                  'total_donations',
                  'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'pk', 'donors',)
# I use this UserSerializer for listing and viewing specific users. 
# I could add a characteristic called lookup_field = 'username' if I want to search by username instead of by pk

class NewUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password',)
# I'm using this class to create new users. I don't entirely understand why, but you have to overwrite the standard create method. I only take in a username and password here, but you can add more fields as arguments in User.objects.create().
```
This sets up our JSON with the fields we want. For some of those fields, we are using a PrimaryKeyRelatedField, which will show up as just a number or an array of numbers. These will correspond to the primary key for the object they are referring to (either users or saved donors). You can see all the available serializers at http://www.django-rest-framework.org/api-guide/serializers/   

## Create Views
Next, go to the ```views.py``` file in the App directory:
```python
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions

from .serializers import SavedDonorSerializer
from .serializers import UserSerializer
from .serializers import NewUserSerializer
from .models import SavedDonor

class SavedDonorList(generics.ListCreateAPIView):
    queryset = SavedDonor.objects.all()
    serializer_class = SavedDonorSerializer

class SavedDonorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedDonor.objects.all()
    serializer_class = SavedDonorSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateAuth(generics.CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = NewUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```
I created different views for CreateAuth (adding a new user), listing users, viewing a specific user, listing donors, and viewing a specific donor.  
The ```generics.``` defines what kind of route it is. ```ListCreateAPIView``` will return a list that allows for POST and GET but no other routes.  ```RetrieveUpdateDestroyAPIView``` will return a view that has full CRUD. The ```CreateAPIView``` is the most basic and requires specifying a model and permissions.  

## Write the URLs
Finally, we go to the ```urls.py``` file in the APP directory (donors/urls.py) and define the routes we want:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('saved-donors',
         views.SavedDonorList.as_view(),
         name='saved-donor-list'),

    path('saved-donors/<int:pk>',
         views.SavedDonorDetail.as_view(),
         name='saved-donor-detail'),

    path('users',
         views.UserList.as_view(),
         name='users-list'),

    path('users/register',
         views.CreateAuth.as_view(),
         name='users-register'),

    path('users/<int:pk>',
         views.UserDetail.as_view(),
         name='user-detail')
         # I could have written the first argument as 'users/<slug:username>' if I wanted to use the username in the URL
]
```
The ```<int:pk>``` refers to the pk search that we may run to get the detail views. Be sure to define the ```int``` as ```pk```, or else it won't work. Once this is done, we can test it. Go to your terminal and run ```python manage.py runserver```. Then go to localhost:8000/api/donors/saved-donors and you should see your list of donors come back!

## Deployment
I'm now going to deploy. I'm going to follow a tutorial at https://simpleisbetterthancomplex.com/tutorial/2016/08/09/how-to-deploy-django-applications-on-heroku.html

