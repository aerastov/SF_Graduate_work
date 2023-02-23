from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('index', Index.as_view()),
    path('info', Info.as_view(), name='info'),
    path('create_car', CreateCar.as_view(), name='create_car'),

]