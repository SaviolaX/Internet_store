from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, ContactForm
from shopping_cart.views import cart_total
from .models import Customer


def user_registration(request):
    """Register new users"""
    form = CreateUserForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password1'])
            new_user_username = user_form.cleaned_data['username']
            new_user_email = user_form.cleaned_data['email']
            new_user_password = user_form.cleaned_data['password1']
            # Save the User object
            new_user.save()
            # Create the user profile
            Customer.objects.create(user=new_user,
                                    name=new_user_username,
                                    email=new_user_email)
            # Login instantly
            user = authenticate(request,
                                username=new_user_username,
                                password=new_user_password)
            login(request, user)
            return redirect('index')
    else:
        user_form = CreateUserForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """Logining user in system"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Your username or password incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def contact_request(request):
    """Saves contact info to database"""
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'We got your request, we will contact you as soon as possible.')
            return redirect('contact')

    total_items_in_order = cart_total(request)

    context = {'form': form, 'total_items_in_order': total_items_in_order}
    return render(request, 'accounts/contact.html', context)
