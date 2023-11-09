# Django for model deployment 
* This is a simple project that deploys an iris flower classification app.

## Architecture Explanation
- A typical Django project has the following structure:
```
project_name
├── project_name
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app_name
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── manage.py
```
* The project_name is the name of the project
* The app_name is the name of the app

### Views
* The views are the functions that are called when a url is visited
* The views are defined in `iris/views.py`
* The views are then mapped to urls in `iris/urls.py`

### urls
* The urls are the urls that are visited
* The urls are defined in `iris/urls.py`
* The urls are then mapped to views in `iris/urls.py`

### admin.py
* The admin.py is the file that is used to register models to the admin page
* The admin.py is defined in `iris/admin.py`

### models.py
* The models.py is the file that is used to define the models in the database (if any)

## manage.py
* The manage.py is the file that is used to run the server
* The manage.py is defined in `manage.py`

### Templates
* The templates are the html files that are rendered when a url is visited
* The templates are defined in `iris/templates/iris`
* The templates are then rendered in the views

## Usage
1. Create a virtual environment (optional)
* `python3 -m venv venv`
* `source venv/bin/activate` 

2. Install requirements
* `pip install -r requirements.txt`

3. Run the server
* `python manage.py runserver`

4. Go to the browser and type the url
* `http://localhost:8000/` (or whatever port you are using)

## Preview
![Preview 1](https://github.com/ashioyajotham/Daily-ML/blob/main/Django%20Model%20Deployment/demo/prev_1.jpeg)
![Preview 2](https://github.com/ashioyajotham/Daily-ML/blob/main/Django%20Model%20Deployment/demo/prev_2.jpeg)


## Important Notes
* The `iris` folder is the app
* The `demo` folder is the project
* The `iris` folder is inside the `demo` folder
* The `iris` folder is the app that is created using `python manage.py startapp iris`
* The `demo` folder is the project that is created using `django-admin startproject demo`

## References
* [Django Documentation](https://docs.djangoproject.com/en/4.2/)
* [Django Tutorial](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
* [Django Tutorial (Youtube)](https://youtu.be/rNhVBv0i4os?si=AGvOBy4oOw5GxpUm)

## Credits
* [Django Tutorial (Youtube)](https://youtu.be/rNhVBv0i4os?si=AGvOBy4oOw5GxpUm)

## QR Code
![QR Code](https://github.com/ashioyajotham/Daily-ML/blob/main/Django%20Model%20Deployment/demo/frame.png)
