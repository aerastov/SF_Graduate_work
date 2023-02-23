from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView
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

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            # print(form.cleaned_data.get("factory_number"))
            self.object_list = Car.objects.filter(factory_number=form.cleaned_data['factory_number'])
            # self.object_list = [list(i.values()) for i in list(Car.objects.filter(factory_number=form.cleaned_data['factory_number']).values())]
        else:
            self.object_list = []

        return self.render_to_response(self.get_context_data(object_list=self.object_list, form=form))


class Info(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'info.html'
    context_object_name = 'cars'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order_by = self.request.GET.get('order_by', 'date_of_shipment_from_the_factory')
        if order_by in ['technique_model', 'engine_model', 'transmission_model', 'drive_axle_model', 'steerable_axle_model']:
            order_by = order_by+"__name"
        print("order_by = ", order_by)
        context['cars'] = []

        if self.request.user.groups.filter(name='admin').exists():
            print("группа admin, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.all
            # context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='manager').exists():
            print("группа manager, user.id = ", self.request.user.id)
            # context['cars'] = Car.objects.all
            context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='service').exists():
            print("группа service, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        elif self.request.user.groups.filter(name='client').exists():
            print("группа client, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        else:
            print("группа не найдена")
            context['cars'] = []

        return context


class Maintenance(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'

class Complaints(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'index.html'
    context_object_name = 'cars'


class CreateCar(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'create_car.html'
    form_class = CreateCarForm
    success_url = '/info'

    # def form_valid(self, form):
    #     # form.save(commit=False)
    #     # car = form.save(commit=False)
    #     # form = self.get_form()
    #     # car.client = User.objects.get(username=form.cleaned_data.get("client"))
    #     # car.save()
    #     return HttpResponseRedirect(reverse('info'))