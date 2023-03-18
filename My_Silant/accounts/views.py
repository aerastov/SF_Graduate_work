from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *
from silant.models import Service_company


class AccountList(PermissionRequiredMixin, ListView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'account_list.html'
    context_object_name = 'users'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['users'] = User.objects.all().order_by('username').order_by('groups')
        return context


class AccountItem(PermissionRequiredMixin, DetailView):
    permission_required = 'auth.view_user'
    model = User
    template_name = 'user_item.html'
    context_object_name = 'user_item'


class CreateAccount(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.add_user'
    model = User
    template_name = 'create_user.html'
    form_class = CreateAccountForm
    success_url = '/accounts/account_list'

    def form_valid(self, form):
        group = form.cleaned_data.get("groups")
        first_name = form.cleaned_data.get("first_name")
        username = form.cleaned_data.get("username")
        id = User.objects.get(username=username).id
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data.get("password"))
        user.save()
        # Сразу создаем новую сервисную компанию в справочнике, если группа = 'service'
        if group.filter(name='service').exists():
            object = Service_company(user_id=id, name=first_name, description="Отсутствует")
            object.save()
        return super().form_valid(form)




class EditAccount(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    template_name = 'update_user.html'
    form_class = UpdateAccountForm
    success_url = '/accounts/account_list'

    def form_valid(self, form):
        form.save()
        # group = form.cleaned_data.get("groups").values('name')[0]['name']
        group = form.cleaned_data.get("groups")
        first_name = form.cleaned_data.get("first_name")
        username = form.cleaned_data.get("username")
        id = User.objects.get(username=username).id
        # Если есть связанная запись в справочнике сервисных компаний, то перезаписываем туда имя компании
        if Service_company.objects.filter(user_id=id).exists():
            service_company = Service_company.objects.get(user_id=id)
            service_company.name = first_name
            service_company.save()
        # Если группа = service, и нет связанной записи в справочнике сервисных к., то создаем запись (если создали
        # аккаунт с другой группой, затем сменили ее на 'service').
        if group.filter(name='service').exists() and not Service_company.objects.filter(user_id=id).exists():
            object = Service_company(user_id=id, name=first_name, description="Отсутствует")
            object.save()
        return super().form_valid(form)


