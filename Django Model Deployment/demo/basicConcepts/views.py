# The basic concept of django is called - MVT ie Model, View, Template
# Model: It is the database layer. It contains the data. It is the data access layer.
# View: It is the business logic layer. It contains the logic of the application.
# Template: It is the presentation layer. It contains the presentation logic of the application.

# The other concept is MVC ie Model, View, Controller
# Model: It is the database layer. It contains the data. It is the data access layer.
# View: It is the presentation layer. It contains the presentation logic of the application.
# Controller: It is the business logic layer. It contains the logic of the application.

# Django follows MVT architecture. It is a variation of MVC architecture.
# In MVT, the controller is replaced by the template.

#from django.http import HttpResponse
from django.shortcuts import render

#def Welcome(request):
    #return HttpResponse("<h1>Welcome to Django</h1>")

def Welcome(request):
    return render(request, "index.html")

def User(request):
    name = request.GET['name']
    print(name)
    return render(request, "user.html", {'name': name})