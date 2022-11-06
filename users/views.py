from .models import Person, User, Career
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth import authenticate, login
from rest_framework import status
from .serializers import serialize_person
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
        avatar_link = ''
        if form_data.get('avatar_link') is not None:
            avatar_link = form_data['avatar_link']
        gender = form_data['gender']
        name = form_data['name']
        surname = form_data['surname']
        patronymic = ''
        if form_data.get('patronymic') is not None:
            patronymic = form_data['patronymic']
        country = form_data['country']
        city = form_data['city']
        birth_date = form_data['birth_date']  # TODO: do format like 29.10.2022 instead of 2022.10.29
        career = Career.objects.get(title=form_data['career'])
        itn = ''
        if form_data.get('itn') is not None:
            itn = form_data['itn']  # TODO: optional field
        user = User.objects.create_user(email, password)
        person = Person.create(user, gender, name, surname,
                               country, city, birth_date, career,
                               itn, avatar_link, patronymic)
        person.save()

        user = authenticate(request, email=email, password=password)
        login(request, user)
        return JsonResponse(status=status.HTTP_201_CREATED,
                            data={
                                'message': 'Signup success',
                                'user_data': serialize_person(person)
                            })
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                        data={
                            'message': 'Bad request'
                        })


@ensure_csrf_cookie
@csrf_exempt
def sign_in(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())

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
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated:
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
    if request.method == 'POST':
        return JsonResponse(status=status.HTTP_200_OK,
                            data={
                                'message': 'Goodbye'
                            })
    return JsonResponse(status=status.HTTP_200_OK,
                        data={
                            'message': 'Hello'
                        })


@csrf_exempt
def get_user_info(request, user_pk):
    if request.method == 'GET':
        try:
            person = Person.objects.get(pk=user_pk)
            return JsonResponse(status=status.HTTP_200_OK,
                                data=serialize_person(person))
        except Person.DoesNotExist:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST,
                                data={
                                    'message': 'Bad request.'
                                })

