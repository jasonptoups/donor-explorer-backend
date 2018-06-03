# Donor Explorer Backend

## Repos

## Assignment
I made this for my final project at General Assembly. This was a solo project. The assignment was to make an app in 1 week using any technologies we wish. I was able to build this app with no instructor-help, instead relying on many, many Google searches.  

You can view my specific process for the backend in the attached markdown called [what-i-did](https://github.com/jasonptoups/donor-explorer-backend/blob/master/what-i-did.md).

## Purpose
The front-end app uses the FEC API to query campaign donor data. It then generates useful calculated fields based on that data. Signed-in users can save donors of interest using this back-end server and access their data in the future. 

## Installation
You can access the deployed front-end at [https://jasonptoups.github.io/donor-explorer/](https://jasonptoups.github.io/donor-explorer/).  

You can access the deployed back-end at various routes on [http://donor-explorer.herokuapp.com/api](http://donor-explorer.herokuapp.com/api). However, please note that most of these routes will require authentication in the near future.  

You can also deploy the backend locally by following these steps:  
1. Fork and Clone this repo
2. In your command line: ```$ cd donor-explorer-backend```
3. In your command line, create and start a virtual environment:
```bash
$ virtualenv .env -p python3
$ source .env/bin/activate
```
3. In your command line, install dependencies: ```$ pip install requirements.txt```
4. Open another command line tab and set up a postgres server:
```bash
$ psql
jasontoups= CREATE DATABASE donor_explorer;
jasontoups= CREATE USER beep WITH PASSWORD 'beepbeep';
jasontoups= GRANT ALL PRIVILEGES ON DATABASE donor_explorer TO beep;
```
5. The current ```settings.py``` file is set up for heroku deployment. You will have to change various settings in order to deploy locally:
```python
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = #PLACE_YOUR_SECRET_KEY_HERE

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FALSE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'donor_explorer',
        'USER': #DB_USERNAME_HERE,
        'PASSWORD': #DB_PASSWORD_HERE,
        'HOST': 'localhost'
    }
}
```
6. Assuming everything has gone smoothly, you can run the server from your command line:
```bash
$ cd donor_explorer
$ python manage.py runserver
```

## Technologies
### Front-end
* Javascript
* HTML
* CSS from Materialize
* React (create-react-app)
* React Router
* JWTs authentication
* Axios (npm package)
* Lodash (npm package)  

### Back-end
* Python
* PostgreSQL
* Django
* Django REST Framework
* Django REST Framework Simple JWTs
* Heroku deployment

### Deployment
The deployed front-end is on github pages while the backend is on Heroku. I am using the free sandbox version of Heroku, so the server sleeps in between frequent use. If you are accessing the deployed version for the first time in a while, please allow a longer wait time after your first API call. 

### Specific Learnings
I taught myself how to set up JWTs on a Django REST Framework for this. I followed several tutorials to do so:
* [Full stack Django: Quick start with JWT auth and React/Redux (Part I-III)](https://medium.com/netscape/full-stack-django-quick-start-with-jwt-auth-and-react-redux-part-i-37853685ab57)
* [Token-based authentication with Django and React](http://geezhawk.github.io/user-authentication-with-react-and-django-rest-framework)     

This was only the second time I have been using Django REST framework, so I learned a lot about that in general. I took detailed notes on all my process steps and wrote them in a markdown file, which you can view in the markdown called [what-i-did](https://github.com/jasonptoups/donor-explorer-backend/blob/master/what-i-did.md). I plan to clean this up a bit and publish it as a simple blog post.  

## Future improvements
There is a lot more that can be improved! The current version is the product of 1 week of work, and I would like to put in more time to really improve it. Some additional changes I would like to make:  
* Protect more routes, requiring authentication
* Improve how I use JWT refresh and access keys. I am currently only using the access key, without a refresh process. I would like to change that. 

## Acknowledgements
Thank you to my instructors and classmates at General Assembly for pushing and inspiring me every day.  

Thank you to everyone who has contributed to the many open-source projects that made this possible  

Thank you to the aforementioned online tutorials.