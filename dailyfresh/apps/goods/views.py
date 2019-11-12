from django.shortcuts import render
from goods import views

# Create your views here.
def index(request):
    '''首页'''
    return render(request, 'index.html')
