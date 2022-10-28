from .models import Person, User, Career
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
# from .serializers import serialize_profile
from django.core import serializers
from django.core.signals import request_started
from django.dispatch import receiver
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

        user = User.objects.create_user(email, password)

        avatar_link = form_data['avatar_link']
        gender = form_data['gender']
        name = form_data['name']
        surname = form_data['surname']
        patronymic = form_data['patronymic']
        country = form_data['country']
        city = form_data['city']
        birth_date = form_data['birth_date']
        career = Career.objects.filter(title=form_data['career'])[0]

        itn = form_data['itn']

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


@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())

        email = form_data['email']
        password = form_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            person = Person.objects.filter(user=user)
            print(serializers.serialize("json", person))
            return JsonResponse(status=status.HTTP_200_OK,
                                data={
                                    'message': serializers.serialize("json", person)
                                })
        else:
            return JsonResponse(status=status.HTTP_401_UNAUTHORIZED,
                                data={
                                    'message': "Your email or password didn't match"
                                })
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'message': 'Bad request'
                        })


