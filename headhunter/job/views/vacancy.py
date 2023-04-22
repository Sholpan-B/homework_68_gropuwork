from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from accounts.models import CustomUser
from job.forms.employer import VacancyForm
from job.models import Vacancy, Resume, Response


class ListVacancyView(LoginRequiredMixin, ListView):
    template_name = 'vacancies/vacancies.html'
    model = Vacancy

    def get(self, request, pk, *args, **kwargs):
        self.user_obj = get_object_or_404(CustomUser, pk=pk)
        vacancy_pk = request.GET.get('vacancy_pk')
        activate = request.GET.get('activate')
        if activate:
            vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
            vacancy.is_active = 1
            vacancy.save()
        deactivate = request.GET.get('deactivate')
        if deactivate:
            vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
            vacancy.is_active = 0
            vacancy.save()
        refresh = request.GET.get('refresh')
        if refresh:
            vacancy = get_object_or_404(Vacancy, pk=vacancy_pk)
            vacancy.save()
        return super(ListVacancyView, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = Vacancy.objects.filter(created_by_id=self.request.user.pk).order_by('-updated_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['user_obj'] = self.user_obj
        return context


class CreateVacancyView(PermissionRequiredMixin, CreateView):
    template_name = 'vacancies/create_vacancy.html'
    model = Vacancy
    form_class = VacancyForm
    permission_required = 'webapp.add_vacancies'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.created_by = request.user
            resume.save()
            return redirect('vacancies', pk=self.request.user.pk)
        context = {'form': form}
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('vacancies', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        return super().has_permission() or self.request.user.is_superuser


class VacancyView(PermissionRequiredMixin, DetailView):
    template_name = 'vacancies/vacancy.html'
    model = Vacancy
    context_object_name = 'vacancy'
    permission_required = 'webapp.view_vacancies'

    def get(self, request, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=kwargs.get('pk'))
        self.user_obj = vacancy.created_by
        refresh = request.GET.get('refresh')
        if refresh:
            vacancy.save()
        return super(VacancyView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        resumes = Resume.objects.filter(author_id=self.request.user.pk, is_active="True")
        kwargs['resumes'] = resumes
        responses = Response.objects.all()
        kwargs['responses'] = responses
        kwargs['user_obj'] = self.user_obj
        return super().get_context_data(**kwargs, form=VacancyForm())


class EditVacancyView(PermissionRequiredMixin, UpdateView):
    template_name = 'vacancies/edit_vacancy.html'
    model = Vacancy
    form_class = VacancyForm
    permission_required = 'webapp.change_vacancies'

    def get_success_url(self):
        return reverse('vacancy', kwargs={'upk': self.request.user.pk, 'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.get_object().created_by == self.request.user \
               or self.request.user.is_superuser


class DeleteVacancyView(PermissionRequiredMixin, DeleteView):
    template_name = 'vacancies/delete_vacancy.html'
    model = Vacancy
    context_object_name = 'vacancy'
    permission_required = 'webapp.delete_vacancies'

    def get_success_url(self):
        return reverse('vacancies', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        return super().has_permission() and self.get_object().created_by == self.request.user \
               or self.request.user.is_superuser
