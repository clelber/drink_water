from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.person_create, name='person_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signup, name='login'),
    path('logged_out/', views.signup, name='logged_out'),
    path('api/create/', views.PersonCreateAPIView.as_view(), name='person_create_api'),
]
