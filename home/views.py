from django.shortcuts import render

# Create your views here.


def index(request):
    ''' A view to return the index page'''
    return render(request, 'home/index.html')


def handle_not_found(request, exception):
    ''' A view to return the 404 page'''
    return render(request, 'home/404.html')
