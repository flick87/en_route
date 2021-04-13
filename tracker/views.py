from django.shortcuts import render

def home(request):
    return render(request, 'tracker/index.html')
