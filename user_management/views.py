from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.
from django.urls import reverse

from user_management.helpers import validator
from user_management.models import SimpleUser
from maps.models import *


def registration(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        second_name = request.POST['second_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        args = {'first_name': first_name, 'second_name': second_name, 'email': email}
        if not validator.is_fields_filled(email, first_name, second_name, password, confirm_password):
            args['error'] = 'Please fill in all fields'
        elif not validator.is_correct_email(email):
            args['error'] = 'Invalid mail format'
        elif not validator.is_email_free(email):
            args['error'] = 'User with this mail already exists'
        elif not validator.is_correct_password(password):
            args['error'] = 'Invalid password format'
        elif not validator.is_passwords_match(password, confirm_password):
            args['error'] = 'Passwords don\'t match'
        elif not validator.is_correct_name(first_name, second_name):
            args['error'] = 'Invalid name format'

        if args.get('error'):
            return args

        user = User(username=email,
                    password=make_password(password, salt=None, hasher='default'),
                    first_name=first_name)

        user.save()
        simple_user = SimpleUser(user=user, second_name=second_name)
        simple_user.save()
        return simple_user


def user_registretion(request):
    if request.method == "POST":
        result = registration(request)
        if isinstance(result, SimpleUser):
            return HttpResponseRedirect(reverse('user_management:login'))
        else:
            return render(request, "user_management/registration.html", result)

    else:
        return render(request, "user_management/registration.html")


def login_view(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect('/profile/')
    user = request.user
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None:
            login(request, user, backend=None)
            if check_status(user) != 'company':
                return HttpResponseRedirect('/profile/')
            else:
                return HttpResponseRedirect('/company/' + user.id)
        else:
            error_message = 'User not found.' if not User.objects.filter(username=request.POST['username']).count() \
                else 'Password incorrect.'
            return render(request, 'user_management/login.html', {'error': error_message,
                                                                  'email': request.POST['username']})
    return render(request, 'user_management/login.html', {'status': check_status(user)})


def check_status(user):
    status = 'student'
    if user is None or user.is_anonymous:
        status = 'anonymous'
    elif user.is_staff:
        status = 'admin'
    return status


def profile(request, user_id=None):
    if request.user.is_anonymous():
        return HttpResponseRedirect('/login/')
    if not user_id:
        if request.user is not None:
            user_id = request.user.id
        else:
            raise Http404('You are not authenticated')
    if SimpleUser.objects.filter(user=User.objects.get(id=user_id)).count():
        user = SimpleUser.objects.get(user=User.objects.get(id=user_id))
        user_lesson = UserLesson.objects.filter(user=user)
    else:
        raise Http404('User with id %s not found.' % user_id)
    return render(request, 'user_management/profile.html',
                  {'user': user, 'results' : user_lesson})