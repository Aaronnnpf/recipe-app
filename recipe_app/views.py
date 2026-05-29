from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipe_index')
        return render(request, 'registration/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'registration/login.html')

def index(request):
    return HttpResponse("You're at the recipe app index.")
