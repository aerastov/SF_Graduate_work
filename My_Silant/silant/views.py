from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.urls import reverse
from django.http import HttpResponseRedirect




class Index(FormMixin, ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'
    form_class = FactoryNumber
    success_url = 'index'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # context['cars'] = Car.objects.all()
        # context['form'] = self.form
        if self.request.user.is_authenticated:
            print("пользователь аутентифицирован")
            context['registered_user'] = User.objects.get(username=self.request.user)
            if self.request.user.groups.filter(name='manager').exists():
                print("группа manager, user.id = ", self.request.user.id)
                context['cars'] = Car.objects.filter(client=self.request.user.id)
            elif self.request.user.groups.filter(name='service').exists():
                print("группа service, user.id = ", self.request.user.id)
                context['cars'] = Car.objects.filter(client=self.request.user.id)
            elif self.request.user.groups.filter(name='client').exists():
                print("группа client, user.id = ", self.request.user.id)
                context['cars'] = Car.objects.filter(client=self.request.user.id)
            else:
                print("группа не найдена")
                context['cars'] = []
        else:
            print("пользователь не аутентифицирован")
            context['registered_user'] = ""  # Если AnonymousUser
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            # print(form.cleaned_data.get("factory_number"))
            self.object_list = Car.objects.filter(factory_number=form.cleaned_data['factory_number'])
            # self.object_list = [list(i.values()) for i in list(Car.objects.filter(factory_number=form.cleaned_data['factory_number']).values())]
            # print("object_list = ", self.object_list)
        else:
            self.object_list = []
        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))


class Info(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'info.html'
    context_object_name = 'cars'

class Maintenance(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'

class Complaints(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'