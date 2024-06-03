from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db import models
from itertools import groupby
from django.db.models import Sum
from .forms import SignUpForm, PersonForm, ConsumptionForm
from rest_framework import generics
from rest_framework.response import Response
from .models import Person, Consumption
from .serializers import PersonSerializer, ConsumptionSerializer
from rest_framework.views import APIView
from django.utils import timezone
from django.utils.dateparse import parse_date


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
        current_date = timezone.now().date()
        daily_goal = person.weight * 35
        total_consumption = Consumption.objects.filter(person=person, date=current_date).aggregate(total=Sum('amount'))['total'] or 0
        remaining_goal = daily_goal - total_consumption
        consumption_percentage = (total_consumption / daily_goal) * 100 if daily_goal != 0 else 0

        data = {
            'id': person.id,
            'name': person.name,
            'weight': person.weight,
            'daily_goal': daily_goal,
            'remaining_goal': remaining_goal,
            'consumption_percentage': consumption_percentage,
            'total_consumption': total_consumption,
            'date': current_date,
        }

        serializer = ConsumptionSerializer(data)
        return Response(serializer.data)


class ConsumptionByDateAPIView(APIView):
    def get(self, request, person_id, date):
        person = Person.objects.get(id=person_id)
        date = parse_date(date)
        daily_consumption = Consumption.objects.filter(person=person, date=date).aggregate(total=Sum('amount'))['total'] or 0
        daily_goal = person.weight * 35
        remaining_goal = daily_goal - daily_consumption
        consumption_percentage = (daily_consumption / daily_goal) * 100 if daily_goal != 0 else 0

        data = {
            'id': person.id,
            'name': person.name,
            'weight': person.weight,
            'daily_goal': daily_goal,
            'remaining_goal': remaining_goal,
            'consumption_percentage': consumption_percentage,
            'total_consumption': daily_consumption,
            'date': date,
        }

        serializer = ConsumptionSerializer(data)
        return Response(serializer.data)


def consumption_details_view(request, person_id):
    person = Person.objects.get(id=person_id)
    consumptions = Consumption.objects.filter(person=person).order_by('-date')

    grouped_consumptions = {}
    for date, items in groupby(consumptions, key=lambda x: x.date):
        grouped_consumptions[date] = list(items)

    detailed_consumptions = []
    for date, items in grouped_consumptions.items():
        total_consumed = sum(item.amount for item in items)
        daily_goal = person.weight * 35
        goal_reached = total_consumed >= daily_goal

        detailed_consumptions.append({
            'date': date,
            'daily_goal': daily_goal,
            'total_consumed': total_consumed,
            'goal_reached': goal_reached
        })

    context = {
        'person': person,
        'detailed_consumptions': detailed_consumptions,
    }
    return render(request, 'accounts/consumption_details.html', context)