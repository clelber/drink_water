from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db import models
from django.db.models import Sum
from .forms import SignUpForm, PersonForm, ConsumptionForm
from rest_framework import generics
from rest_framework.response import Response
from .models import Person, Consumption
from .serializers import PersonSerializer, ConsumptionSerializer
from rest_framework.views import APIView
from django.utils import timezone


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home.html')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def person_create(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return redirect('consumption_view', person_id=person.id)
    else:
        form = PersonForm()
    return render(request, 'accounts/person_form.html', {'form': form})


class PersonCreateAPIView(generics.CreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


def consumption_view(request, person_id):
    person = Person.objects.get(id=person_id)
    if request.method == 'POST':
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            consumption = form.save(commit=False)
            consumption.person = person
            consumption.save()
            return redirect('consumption_view', person_id=person_id)
    else:
        form = ConsumptionForm()

    current_date = timezone.now().date()

    daily_goal = person.weight * 35

    total_consumption = Consumption.objects.filter(person=person).aggregate(total=models.Sum('amount'))['total'] or 0

    remaining_goal = daily_goal - total_consumption

    if daily_goal != 0:
        consumption_percentage = (total_consumption / daily_goal) * 100
    else:
        consumption_percentage = 0

    context = {
        'form': form,
        'total_consumption': total_consumption,
        'person': person,
        'daily_goal': daily_goal,
        'remaining_goal': remaining_goal,
        'consumption_percentage': consumption_percentage,
        'date': current_date,
    }
    return render(request, 'accounts/consumption.html', context)


class ConsumptionAPIView(APIView):
    def get(self, request, person_id):
        person = Person.objects.get(id=person_id)

        # Calcular a meta do dia
        daily_goal = person.weight * 35

        # Calcular a meta já consumida
        total_consumption = Consumption.objects.filter(person=person).aggregate(total=Sum('amount'))['total'] or 0

        # Calcular a meta restante
        remaining_goal = daily_goal - total_consumption

        # Calcular a porcentagem da meta já consumida
        consumption_percentage = (total_consumption / daily_goal) * 100 if daily_goal != 0 else 0

        data = {
            'id': person.id,
            'name': person.name,
            'weight': person.weight,
            'daily_goal': daily_goal,
            'remaining_goal': remaining_goal,
            'consumption_percentage': consumption_percentage,
            'total_consumption': total_consumption,
        }

        serializer = ConsumptionSerializer(data)
        return Response(serializer.data)
