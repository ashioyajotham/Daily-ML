# Django for model deployment 
* This is a simple project that deploys an iris flower classificatio app

## Architecture Explanation
- A typical Django project has the following structure
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
