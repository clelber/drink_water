from django.shortcuts import render


def home(request):
    return render(request, 'person_create.html')
