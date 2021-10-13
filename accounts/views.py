from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm, ContactForm
from shopping_cart.views import cart_total
from django.contrib import messages


def user_registration(request):
    """Register new users"""
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(data=request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('index')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_login(request):
    """Logining user in system"""
    if request.user.is_authenticated:
        return redirect('index')
    else:
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
