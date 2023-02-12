from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import *

class Index(ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['list_in_page'] = self.paginate_by
        if self.request.user.is_authenticated:
            context['registered_user'] = User.objects.get(username=self.request.user)
        else:
            context['registered_user'] = ""  # Если AnonymousUser
        return context