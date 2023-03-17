from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import FormMixin, CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from .forms import *


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
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data.get("password"))
        user.save()
        return super().form_valid(form)

class EditAccount(PermissionRequiredMixin, UpdateView):
    permission_required = 'auth.change_user'
    model = User
    template_name = 'update_user.html'
    form_class = UpdateAccountForm
    success_url = '/accounts/account_list'

    def form_valid(self, form):
        user = form.save(commit=False)
        # print('groups = ', form.cleaned_data.get("groups"))
        # user.groups = list(form.cleaned_data.get("groups"))
        # group = Group.objects.get(name=form.cleaned_data.get("groups"))
        # self.groups.add(group)
        #
        # user.save()
        return super().form_valid(form)


