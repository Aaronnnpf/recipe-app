from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CommentForm, RecipeForm
from .models import Comment, Recipe


def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipe_index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # If "Remember me" is checked, set session to persist for 30 days
            if remember:
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30 days in seconds
            return redirect('recipe_index')
        return render(
            request,
            'registration/login.html',
            {'error': 'Invalid username or password.'}
        )

    return render(request, 'registration/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('recipe_index')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1 or not password2:
            error = 'All fields are required.'
        elif password1 != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'A user with that username already exists.'
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
            )
            login(request, user)
            return redirect('recipe_index')

    return render(request, 'registration/signup.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def recipe_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.all()
    form = CommentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        comment = form.save(commit=False)
        comment.recipe = recipe
        comment.author = request.user
        comment.save()
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'form': form,
    })


def recipe_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    form = RecipeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Create Recipe',
    })


def recipe_edit(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return HttpResponse(
            'You are not allowed to edit this recipe.',
            status=403,
        )

    form = RecipeForm(request.POST or None, instance=recipe)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Edit Recipe',
    })


def recipe_delete(request, recipe_id):
    if not request.user.is_authenticated:
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return HttpResponse(
            'You are not allowed to delete this recipe.',
            status=403,
        )

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_index')

    return render(request, 'recipes/recipe_confirm_delete.html', {
        'recipe': recipe,
    })


def comment_delete(request, recipe_id, comment_id):
    if not request.user.is_authenticated:
        return redirect('login')

    recipe = get_object_or_404(Recipe, id=recipe_id)
    comment = get_object_or_404(Comment, id=comment_id, recipe=recipe)

    if comment.author != request.user:
        return HttpResponse(
            'You are not allowed to delete this comment.',
            status=403,
        )

    if request.method == 'POST':
        comment.delete()
    return redirect('recipe_detail', recipe_id=recipe.id)
