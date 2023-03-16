from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.models import User



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




# class Account(LoginRequiredMixin, TemplateView):
class Account(TemplateView):
    template_name = 'account.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context