from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from job.forms.candidate import EducationForm
from job.models import Education, Resume


class CreateEducationView(PermissionRequiredMixin, CreateView):
    template_name = 'educations/create_education.html'
    model = Education
    form_class = EducationForm
    permission_required = 'webapp.add_educations'

    def post(self, request, upk, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        resume = get_object_or_404(Resume, pk=pk)
        if form.is_valid():
            education = form.save(commit=False)
            education.save()
            resume.education.add(education)
            return redirect('resume', upk=upk, pk=pk)
        context = {'form': form}
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('pk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)


class EditEducationView(PermissionRequiredMixin, UpdateView):
    template_name = 'educations/edit_education.html'
    model = Education
    form_class = EducationForm
    permission_required = 'webapp.change_educations'

    def get_success_url(self):
        return reverse('resume', kwargs={'upk': self.request.user.pk, 'pk': self.kwargs.get('rpk')})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('rpk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)


class DeleteEducationView(PermissionRequiredMixin, DeleteView):
    template_name = 'educations/delete_education.html'
    model = Education
    context_object_name = 'education'
    permission_required = 'webapp.delete_educations'

    def get(self, request, *args, **kwargs):
        self.resume_pk = kwargs.get('rpk')
        return super(DeleteEducationView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['resume_pk'] = self.resume_pk
        return super(DeleteEducationView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('resume', kwargs={'upk': self.request.user.pk, 'pk': self.kwargs.get('rpk')})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('rpk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)
