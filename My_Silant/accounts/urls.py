from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    # path('account/', Account.as_view()),

    # path('edit/', Update_profile.as_view(template_name = 'sign/update_profile.html'), name='user_update'),
    # path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
    path('', include('allauth.urls')),
    path('account_list', AccountList.as_view(), name='account_list'),
    path('account_list/<int:pk>', AccountItem.as_view()),

]


# urlpatterns = [
#   path('profile', account_profile, name='account_profile'),
#   path('update', EditProfile.as_view(), name='account_update'),
# ]
