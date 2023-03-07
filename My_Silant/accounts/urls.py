from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    # path('account/', Account.as_view()),
    # path('add_authors/', add_authors, name = 'upgrade'),
    # path('login/', LoginView.as_view(template_name = 'sign/login.html'), name='login'),
    # path('logout/', LogoutView.as_view(template_name = 'sign/logout.html'), name='logout'),
    # path('edit/', Update_profile.as_view(template_name = 'sign/update_profile.html'), name='user_update'),
    # path('signup/', BaseRegisterView.as_view(template_name = 'sign/signup.html'), name='signup'),
    path('', include('allauth.urls')),
]


# urlpatterns = [
#   path('profile', account_profile, name='account_profile'),
#   path('update', EditProfile.as_view(), name='account_update'),
# ]
