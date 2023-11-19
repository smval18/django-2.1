from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from . import models
from . import forms

from django.contrib.auth import mixins
from django.views.generic import edit
from django.core.exceptions import PermissionDenied
from .mixins import AdminRequiredMixin


class IndexView(generic.View):
    def get(self, request):
        return render(request, 'index.html', self.get_context_data())

    def get_context_data(self):
        context = {
            'new_applications': models.Application.get_new_applications(),
            'accept_applications': models.Application.get_accept_applications(),
            'accept_applications_count': models.Application.get_accept_applications_count(),
            'done_applications': models.Application.get_done_applications(),
            'applications_count': models.Application.get_count(),
        }

        return context


class RegisterView(generic.CreateView):
    model = User
    form_class = forms.RegisterForm
    template_name = 'registration/register.html'

    success_url = reverse_lazy('login')


def logouted(request):
    return render(request, 'registration/logout.html')


class ProfileView(mixins.LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'registration/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


class MyAppsView(mixins.LoginRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'my_application.html', self.get_context_data())

    def get_context_data(self):
        filters = {
            'user': self.request.user,
        }

        if self.request.GET.get('status'):
            filters['status'] = models.Status.objects.get(
                name=self.request.GET.get('status'))

        context = {
            'statuses': models.Status.objects.all(),
            'applications': models.Application.objects.filter(**filters).order_by('-created_at').all(),
        }

        return context


class NewAppView(mixins.LoginRequiredMixin, edit.CreateView):
    model = models.Application
    form_class = forms.NewApplicationForm
    template_name = 'new_application.html'
    success_url = reverse_lazy('myapplication')

    def get_form_kwargs(self):
        kwargs = super(NewAppView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeleteAppView(mixins.LoginRequiredMixin, edit.DeleteView):
    model = models.Application
    success_url = reverse_lazy('myapplication')
    template_name = 'delete_application.html'

    def get_object(self, queryset=None):
        obj = super(DeleteAppView, self).get_object()

        if obj.user != self.request.user or obj.status != models.Status.get_by_name('новая'):
            raise PermissionDenied

        return obj


class AdminPanelView(AdminRequiredMixin, generic.View):
    def get(self, request):
        return render(request, 'superadmin/index.html', self.get_context_data())

    def get_context_data(self):
        context = {}

        return context


class CategoriesListView(AdminRequiredMixin, generic.ListView):
    model = models.Category
    template_name = 'superadmin/categories.html'
    context_object_name = 'categories'


class CategoryCreateView(AdminRequiredMixin, generic.CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = 'superadmin/category_create.html'
    success_url = reverse_lazy('admin-categories')


class ApplicationsListView(AdminRequiredMixin, generic.ListView):
    model = models.Application
    template_name = 'superadmin/applications.html'
    context_object_name = 'applications'


class CategoryDeleteView(mixins.LoginRequiredMixin, edit.DeleteView):
    model = models.Category
    success_url = reverse_lazy('admin-categories')
    template_name = 'superadmin/category_delete.html'
