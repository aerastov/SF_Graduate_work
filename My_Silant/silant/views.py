from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

    def get_queryset(self):
        return []

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


class Info(PermissionRequiredMixin, ListView):
    permission_required = 'silant.view_car'
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
            context['cars'] = Car.objects.all().order_by(order_by)
            # context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='manager').exists():
            print("группа manager, user.id = ", self.request.user.id)
            # context['cars'] = Car.objects.all
            context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='service').exists():
            print("группа service, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        elif self.request.user.groups.filter(name='client').exists():
            print("группа client, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        else:
            print("группа не найдена")
            context['cars'] = []

        return context


class InfoItem(PermissionRequiredMixin, DetailView):
    permission_required = 'silant.view_car'
    model = Car
    template_name = 'car_item.html'
    context_object_name = 'car'


class CreateCar(PermissionRequiredMixin, CreateView):
    permission_required = 'silant.add_car'
    model = Car
    template_name = 'create_car.html'
    form_class = CreateCarForm
    success_url = '/info'


class EditCar(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_car'
    model = Car
    template_name = 'create_car.html'
    form_class = CreateCarForm
    success_url = '/info'


class DeleteCar(PermissionRequiredMixin, DeleteView):
    permission_required = 'silant.delete_car'
    model = Car
    template_name = 'delete_car.html'
    success_url = '/info'


class Maintenance(PermissionRequiredMixin, ListView):
    permission_required = 'silant.view_maintenance'
    model = Maintenance
    template_name = 'maintenance.html'
    context_object_name = 'maintenances'



class CreateMaintenances(PermissionRequiredMixin, CreateView):
    permission_required = 'silant.add_maintenance'
    model = Maintenance
    template_name = 'create_maintenance.html'
    form_class = CreateMaintenancesForm
    success_url = '/maintenance'
    context_object_name = 'cars'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        id = self.request.GET.get('id', '---')
        if "---" in id:
            context['select_car'] = "---"
        else:
            context['select_car'] = Car.objects.get(id=id)

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(name='manager').exists():
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = Car.objects.all(client='self.request.user')
        return context

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '---')
        if "---" in id:
            kwargs['initial'] = {'select_car': ""}
        else:
            service_company = Car.objects.get(id=id).service_company
            kwargs['initial'] = {'service_company': service_company}
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        return kwargs






class Complaints(PermissionRequiredMixin, ListView):
    permission_required = 'silant.view_complaints'
    model = Complaints
    template_name = 'index.html'
    context_object_name = 'cars'












# class SelectCarMaintenance(PermissionRequiredMixin, ListView):
#     permission_required = 'silant.add_maintenance'
#     model = Car
#     template_name = 'select_car.html'
#     context_object_name = 'cars'
#
#     def get_queryset(self):
#         if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(name='manager').exists():
#             list_cars = Car.objects.all()
#         else:
#             list_cars = Car.objects.all(client='self.request.user')
#         return list_cars
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         order_by = self.request.GET.get('order_by', 'service_company')
#         if order_by in ['technique_model']:
#             order_by = order_by+"__name"
#         context['cars'] = context['cars'].order_by(order_by)
#         return context