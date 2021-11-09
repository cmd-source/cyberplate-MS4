from django.shortcuts import render

# Create your views here.


def shopping_bag(request):
    ''' A view to return the users shopping bag page'''
    return render(request, 'shopping_bag.html')
