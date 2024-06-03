from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.person_create, name='person_create'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.signup, name='login'),
    path('logged_out/', views.signup, name='logged_out'),
    path('api/create/', views.PersonCreateAPIView.as_view(), name='person_create_api'),
    path('consume/<int:person_id>/', views.consumption_view, name='consumption_view'),
    path('api/consumption/<int:person_id>/', views.ConsumptionAPIView.as_view(), name='consumption_api'),
    path('api/consumption/<int:person_id>/<str:date>/', views.ConsumptionByDateAPIView.as_view(), name='consumption_by_date_api'),
    path('accounts/consume/details/<int:person_id>/', views.consumption_details_view, name='consumption_details'),
]
