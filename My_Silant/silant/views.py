from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
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
        # print("order_by = ", order_by)
        context['cars'] = []

        if self.request.user.groups.filter(name='admin').exists():
            # print("группа admin, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.all().order_by(order_by)
            # context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='manager').exists():
            # print("группа manager, user.id = ", self.request.user.id)
            # context['cars'] = Car.objects.all
            context['cars'] = Car.objects.all().order_by(order_by)
        elif self.request.user.groups.filter(name='service').exists():
            # print("группа service, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        elif self.request.user.groups.filter(name='client').exists():
            # print("группа client, user.id = ", self.request.user.id)
            context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
            # context['cars'] = Car.objects.filter(client=self.request.user.id).order_by(order_by)
        else:
            # print("группа не найдена")
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
    template_name = 'update.html'
    form_class = CreateCarForm
    success_url = '/info'


class DeleteCar(PermissionRequiredMixin, DeleteView):
    permission_required = 'silant.delete_car'
    model = Car
    template_name = 'delete.html'
    success_url = '/info'


class MaintenanceList(PermissionRequiredMixin, ListView):
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
        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "---------"
        else:
            context['select_car'] = Car.objects.get(id=id)

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(name='manager').exists():
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = Car.objects.all(client='self.request.user')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')
        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = Car.objects.get(id=id).service_company_id
            kwargs['initial'] = {'service_company': service_company, 'car': id}
        return kwargs


class MaintenanceItem(PermissionRequiredMixin, DetailView):
    permission_required = 'silant.view_maintenance'
    model = Maintenance
    template_name = 'maintenance_item.html'
    context_object_name = 'maintenance'


class MaintenanceEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_maintenance'
    model = Maintenance
    template_name = 'update.html'
    form_class = UpdateMaintenancesForm
    success_url = '/maintenance'


class MaintenanceDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'silant.delete_maintenance'
    model = Maintenance
    template_name = 'delete.html'
    success_url = '/maintenance'


class ComplaintsList(PermissionRequiredMixin, ListView):
    permission_required = 'silant.view_complaints'
    model = Complaints
    template_name = 'complaints.html'
    context_object_name = 'complaints'



class CreateComplaints(PermissionRequiredMixin, CreateView):
    permission_required = 'silant.add_complaints'
    model = Complaints
    template_name = 'create_complaints.html'
    form_class = CreateComplaintsForm
    success_url = '/complaints'
    context_object_name = 'cars'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        id = self.request.GET.get('id', '')
        if id == '':
            context['select_car'] = "---------"
        else:
            context['select_car'] = Car.objects.get(id=id)

        if self.request.user.groups.filter(name='admin').exists() or self.request.user.groups.filter(name='manager').exists():
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = Car.objects.all(client='self.request.user')
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        id = self.request.GET.get('id', '')
        if id == '':
            kwargs['initial'] = {'service_company': ""}
        else:
            service_company = Car.objects.get(id=id).service_company_id
            kwargs['initial'] = {'service_company': service_company, 'car': id}
        return kwargs



class ComplaintsItem(PermissionRequiredMixin, DetailView):
    permission_required = 'silant.view_complaints'
    model = Complaints
    template_name = 'complaints_item.html'
    context_object_name = 'complaints'


class ComplaintsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_complaints'
    model = Complaints
    template_name = 'update.html'
    form_class = UpdateComplaintsForm
    success_url = '/complaints'


class ComplaintsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'silant.delete_complaints'
    model = Complaints
    template_name = 'delete.html'
    success_url = '/complaints'


def reference_book(request):
    return render(request, 'reference_book.html')


class ReferenceBookList(PermissionRequiredMixin, TemplateView):
    permission_required = 'silant.view_technique_model, silant.view_engine_model, silant.view_transmission_model,' \
                          ' silant.view_drive_axle_model, silant.view_steerable_axle_model, silant.view_service_company,' \
                          ' silant.view_type_maintenance, silant.view_description_failure, silant.view_recovery_method'
    template_name = 'reference_book_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if pk == 1:
            context['name'] = "Модель техники"
            context['list'] = Technique_model.objects.all()
        elif pk == 2:
            context['name'] = "Модель двигателя"
            context['list'] = Engine_model.objects.all()
        elif pk == 3:
            context['name'] = "Модель трансмиссии"
            context['list'] = Transmission_model.objects.all()
        elif pk == 4:
            context['name'] = "Модель ведущего моста"
            context['list'] = Drive_axle_model.objects.all()
        elif pk == 5:
            context['name'] = "Модель управляемого моста"
            context['list'] = Steerable_axle_model.objects.all()
        elif pk == 6:
            context['name'] = "Сервисная организация"
            context['list'] = Service_company.objects.all()
        elif pk == 7:
            context['name'] = "Вид ТО"
            context['list'] = Type_maintenance.objects.all()
        elif pk == 8:
            context['name'] = "Характер отказа"
            context['list'] = Description_failure.objects.all()
        elif pk == 9:
            context['name'] = "Способ восстановления"
            context['list'] = Recovery_method.objects.all()
        return context


class TechniqueModelEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_technique_model'
    model = Technique_model
    template_name = 'update.html'
    form_class = UpdateTechniqueModelForm
    success_url = '../'


class EngineModelEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_engine_model'
    model = Engine_model
    template_name = 'update.html'
    form_class = UpdateEngineModelForm
    success_url = '../'


class TransmissionModelEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_transmission_model'
    model = Transmission_model
    template_name = 'update.html'
    form_class = UpdateTransmissionModelForm
    success_url = '../'


class DriveAxleModelEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_drive_axle_model'
    model = Drive_axle_model
    template_name = 'update.html'
    form_class = UpdateDriveAxleModelForm
    success_url = '../'


class SteerableAxleModelEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_steerable_axle_model'
    model = Steerable_axle_model
    template_name = 'update.html'
    form_class = UpdateSteerableAxleModelForm
    success_url = '../'


class ServiceCompanyEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_service_company'
    model = Service_company
    template_name = 'update.html'
    form_class = UpdateServiceCompanyForm
    success_url = '../'


class TypeMaintenanceEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_type_maintenance'
    model = Type_maintenance
    template_name = 'update.html'
    form_class = UpdateTypeMaintenanceForm
    success_url = '../'


class DescriptionFailureEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_description_failure'
    model = Description_failure
    template_name = 'update.html'
    form_class = UpdateDescriptionFailureForm
    success_url = '../'


class RecoveryMethodEdit(PermissionRequiredMixin, UpdateView):
    permission_required = 'silant.change_recovery_method'
    model = Recovery_method
    template_name = 'update.html'
    form_class = UpdateRecoveryMethodForm
    success_url = '../'
