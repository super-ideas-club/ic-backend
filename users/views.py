from .models import Person, User, Career
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect, ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from .serializers import serialize_person
from django.core import serializers
import json


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())

        email = form_data['email']
        password = form_data['password']

        if User.objects.filter(email=email).exists():
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'message': 'Email already taken!'
                                })

        avatar_link = form_data['avatar_link']  # TODO: optional field
        gender = form_data['gender']
        name = form_data['name']
        surname = form_data['surname']
        patronymic = form_data['patronymic']  # TODO: optional field
        country = form_data['country']
        city = form_data['city']
        birth_date = form_data['birth_date']  # TODO: do format like 29.10.2022 instead of 2022.10.29
        career = Career.objects.filter(title=form_data['career'])[0]

        itn = form_data['itn']  # TODO: optional field
        user = User.objects.create_user(email, password)
        person = Person.create(user, gender, name, surname,
                               country, city, birth_date, career,
                               itn, avatar_link, patronymic)
        person.save()

        return JsonResponse(status=status.HTTP_201_CREATED,
                            data={
                                'message': 'Signup success'
                            })
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'message': 'Bad request'
                        })


@ensure_csrf_cookie
@csrf_exempt
def sign_in(request):
    print(request.method)
    print(request.body)
    print(request.body.decode())
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())
        print(form_data)

        email = form_data['email']
        password = form_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            person = Person.objects.filter(user=user)[0]
            return JsonResponse(status=status.HTTP_200_OK,
                                data=serialize_person(person))
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,
                                data={
                                    'message': "Your email or password didn't match"
                                })
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'message': 'Bad request'
                        })


@xframe_options_exempt
@csrf_exempt  # TODO: maybe change to @csrf_exempt if have no time
def get_data(request):
    print(request.method)
    if request.method == 'GET':
        user = request.user
        print("alo")
        if user.is_authenticated:
            print("alo2")
            person = Person.objects.filter(user=user)[0]
            return JsonResponse(status=status.HTTP_200_OK,
                                data=serialize_person(person))  # TODO: fix serializer maybe
        return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,
                            data={
                                'message': 'User unauthorized.'
                            })
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'message': 'Bad request.'
                        })


@xframe_options_exempt
@csrf_exempt
def test_view(request):
    print(request.method)
    if request.method == 'POST':
        return JsonResponse(status=status.HTTP_200_OK,
                            data={
                                'message': 'Goodbye'
                            })
    return JsonResponse(status=status.HTTP_200_OK,
                        data={
                            'message': 'Hello'
                        })




