from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from job.forms.candidate import ExperienceForm
from job.models import WorkExperience, Resume


class CreateExperienceView(PermissionRequiredMixin, CreateView):
    template_name = 'experiences/create_experience.html'
    model = WorkExperience
    form_class = ExperienceForm
    permission_required = 'webapp.add_experiences'

    def post(self, request, upk, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        resume = get_object_or_404(Resume, pk=pk)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.save()
            resume.work_experience.add(experience)
            return redirect('resume', upk=upk, pk=pk)
        context = {'form': form}
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('profile', kwargs={'upk': self.request.user.pk})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('pk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)


class EditExperienceView(PermissionRequiredMixin, UpdateView):
    template_name = 'experiences/edit_experience.html'
    model = WorkExperience
    form_class = ExperienceForm
    permission_required = 'webapp.change_experiences'

    def get_success_url(self):
        return reverse('resume', kwargs={'upk': self.request.user.pk, 'pk': self.kwargs.get('rpk')})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('rpk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)


class DeleteExperienceView(PermissionRequiredMixin, DeleteView):
    template_name = 'experiences/delete_experience.html'
    model = WorkExperience
    context_object_name = 'experience'
    permission_required = 'webapp.delete_experiences'

    def get(self, request, *args, **kwargs):
        self.resume_pk = kwargs.get('rpk')
        return super(DeleteExperienceView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['resume_pk'] = self.resume_pk
        return super(DeleteExperienceView, self).get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('resume', kwargs={'upk': self.request.user.pk, 'pk': self.kwargs.get('rpk')})

    def has_permission(self):
        resume = get_object_or_404(Resume, pk=self.kwargs.get('rpk'))
        return (super().has_permission() or resume.created_by.username == str(self.request.user)
                or self.request.user.is_superuser)
