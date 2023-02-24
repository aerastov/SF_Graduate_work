from django.urls import path
from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('index', Index.as_view()),
    path('info', Info.as_view(), name='info'),
    path('info/<int:pk>', InfoItem.as_view()),
    # path('info/<int:pk>/edit', InfoEdit.as_view()),
    # path('info/<int:pk>/delete', InfoDelete.as_view()),
    path('create_car', CreateCar.as_view(), name='create_car'),

]