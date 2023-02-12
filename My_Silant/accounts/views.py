from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# class Account(LoginRequiredMixin, TemplateView):
class Account(TemplateView):
    template_name = 'account.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context