from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.utils import dateformat
from django.http import HttpResponse
from rest_framework import generics, status, permissions, mixins, serializers
from rest_framework.response import Response
from datetime import datetime as dt
from . import forms
import json
import requests
from weather_forecast import settings
from drf_spectacular.utils import extend_schema, inline_serializer
from .models import History
from .serializers import RegistrationSerializer, UserSerializer, UserEditSerializer


# Регистрация через API
class RegistrationAPIView(generics.GenericAPIView):
    """
    Представление для регистрации пользователя
    Доступ к данному эндпоинту всем.
    """
    serializer_class = RegistrationSerializer
    @extend_schema(
        summary="Регистрация пользователя.",
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                name='register_201',
                fields={"message": serializers.CharField(default="Пользователь успешно зарегистрирован.")},
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='register_400',
                fields={"message": serializers.CharField(default="Сообщение об ошибке.")},
            ),
        },
        tags=["registration"],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": 'Пользователь успешно зарегистрирован.'},
            status=status.HTTP_201_CREATED,
        )

# Регистрация через Django формы
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('weather')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@extend_schema(
    summary="Личный кабинет пользователя.",
    tags=["auth"],
)
class UserDetailView(mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Представление для получения данных авторизованного пользователя.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        description="Получение данных авторизованного пользователя.",
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='user_detail_400',
                fields={"message": serializers.CharField(default="Сообщение об ошибке.")},
            ),
        },
    )
    def get(self, request):
        data = self.serializer_class(request.user).data
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Изменение данных авторизованного пользователя.",
        request=UserEditSerializer,
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                name='user_patch_400',
                fields={"message": serializers.CharField(default="Сообщение об ошибке.")},
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        serializer = UserEditSerializer(request.user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Данные пользователя обновлены."},
            status=status.HTTP_200_OK
        )

@login_required
def weather_forecast(request):

    if request.method == 'POST':
        forecast_form = forms.ForecastForm(request, request.POST)

        if forecast_form.is_valid():
            city = forecast_form.cleaned_data['city']
            if not city:
                city = forecast_form.cleaned_data['history']

            if city.startswith('г '):
                city = city[2:]

            days = int(forecast_form.cleaned_data['days'])
            access_key = settings.ACCESS_KEY
            yandex_geocode = settings.YANDEX_GEOCODE
            dadata_token = settings.DADATA_TOKEN
            headers = {
                'X-Yandex-Weather-Key': access_key
            }
            response = requests.get(f'https://geocode-maps.yandex.ru/1.x?apikey={yandex_geocode}&format=json&geocode={city}')
            json_response = response.json()
            try:
                # Получаем координаты города(долгота и широта)
                lon, lat = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()

                History.objects.create(
                    user=request.user,
                    city=city
                )

            except (IndexError, KeyError):
                return HttpResponse('Город не найден')

            # Получаем массив данных по погоде
            res = requests.get(
                f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU',
                headers=headers
            )
            weather = json.loads(res.text)

            city_info = []
            
            for day_week in range(days):
                if day_week < len(weather['forecasts']):
                    # Переделал дату в удобный формат
                    date = dt.strptime(weather['forecasts'][day_week]['date'], '%Y-%m-%d')
                    date = dateformat.format(date, 'l-d E Y')
                    weekday, date = date.split('-')

                    day_info = {
                        'city': city,
                        'weekday': weekday,
                        'date': date,
                        'icon': weather['forecasts'][day_week]['parts']['day_short']['icon'],
                        'temp': weather['forecasts'][day_week]['parts']['day_short']['temp'],
                        'feels_like': weather['forecasts'][day_week]['parts']['day_short']['feels_like'],
                        'wind_speed': weather['forecasts'][day_week]['parts']['day_short']['wind_speed']
                    }
                    city_info.append(day_info)
    
            forecast_form = forms.ForecastForm(request)
            
            context = {
                'forecast_form': forecast_form,
                'city_info': city_info,
                'city': city,
                'days': days,
                'dadata_token': dadata_token,
            }
            return render(request, 'index.html', context=context)
    forecast_form = forms.ForecastForm(request)
    return render(request, 'index.html', {'forecast_form': forecast_form})
