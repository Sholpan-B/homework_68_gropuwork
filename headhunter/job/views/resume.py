from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from accounts.models import CustomUser
from job.forms.candidate import ResumeForm
from job.models import Resume, Vacancy, Response


class CreateResumeView(PermissionRequiredMixin, CreateView):
    template_name = 'resumes/create_resume.html'
    model = Resume
    form_class = ResumeForm
    permission_required = 'webapp.add_resumes'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.created_by = request.user
            resume.save()
            return redirect('resumes', pk=self.request.user.pk)
        context = {'form': form}
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('resumes', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        return super().has_permission() or self.request.user.is_superuser


class ListResumesView(LoginRequiredMixin, ListView):
    template_name = 'resumes/resumes.html'
    model = Resume

    def get(self, request, pk, *args, **kwargs):
        self.user_obj = get_object_or_404(CustomUser, pk=pk)
        resume_pk = request.GET.get('resume_pk')
        activate = request.GET.get('activate')
        if activate:
            resume = get_object_or_404(Resume, pk=resume_pk)
            resume.is_active = 1
            resume.save()
        deactivate = request.GET.get('deactivate')
        if deactivate:
            resume = get_object_or_404(Resume, pk=resume_pk)
            resume.is_active = 0
            resume.save()
        refresh = request.GET.get('refresh')
        if refresh:
            resume = get_object_or_404(Resume, pk=resume_pk)
            resume.save()
        return super(ListResumesView, self).get(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = Resume.objects.filter(created_by_id=self.request.user.pk).order_by('-updated_at')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['user_obj'] = self.user_obj
        return context


class ResumeView(LoginRequiredMixin, DetailView):
    template_name = 'resumes/resume.html'
    model = Resume
    context_object_name = 'resume'

    def get(self, request, *args, **kwargs):
        resume = get_object_or_404(Resume, pk=kwargs.get('pk'))
        self.user_obj = resume.created_by
        refresh = request.GET.get('refresh')
        if refresh:
            resume.save()
        return super(ResumeView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        vacancy = Vacancy.objects.filter(author_id=self.request.user.pk, is_active="True")
        kwargs['vacancies'] = vacancy
        responses = Response.objects.all()
        kwargs['responses'] = responses
        kwargs['user_obj'] = self.user_obj
        return super().get_context_data(**kwargs, form=ResumeForm())


class EditResumeView(PermissionRequiredMixin, UpdateView):
    template_name = 'resumes/edit_resume.html'
    model = Resume
    form_class = ResumeForm
    permission_required = 'webapp.change_resumes'

    def get_success_url(self):
        return reverse('resume', kwargs={'upk': self.request.user.pk, 'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.get_object().author == self.request.user \
               or self.request.user.is_superuser


class DeleteResumeView(PermissionRequiredMixin, DeleteView):
    template_name = 'resumes/delete_resume.html'
    model = Resume
    context_object_name = 'resume'
    permission_required = 'webapp.delete_resumes'

    def get_success_url(self):
        return reverse('resumes', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        return super().has_permission() and self.get_object().author == self.request.user \
               or self.request.user.is_superuser
