from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from accounts.models import CustomUser
from job.forms.employer import ResponseMessageForm
from job.models import Response, ResponseMessage


class ResponseListView(ListView):
    template_name = 'response/responses_list.html'
    model = Response
    context_object_name = 'responses'


class ResponseView(DetailView):
    template_name = 'response/response.html'
    model = Response
    context_object_name = 'response'

    def get(self, request, *args, **kwargs):
        self.extra_context = {'message_form': ResponseMessageForm()}
        return super().get(request, *args, **kwargs)


class AddResponseMessageView(CreateView):
    model = ResponseMessage
    form_class = ResponseMessageForm
    template_name = 'response/response.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_pk = kwargs.get('upk')
        resume_pk = kwargs.get('rpk')
        response_pk = kwargs.get('pk')
        if form.is_valid():
            response_message = form.save(commit=False)
            response_message.response = get_object_or_404(Response, pk=response_pk)
            response_message.responded_by = get_object_or_404(CustomUser, pk=user_pk)
            response_message.save()
            return redirect('response', user_pk, resume_pk, response_pk)
        return redirect('response', user_pk, resume_pk, response_pk)


class DeleteResponseMessageView(DeleteView):
    template_name = 'response/delete_message.html'
    model = ResponseMessage
    context_object_name = 'response_message'

    def get_success_url(self):
        return reverse('job:response',
                       kwargs={
                           'upk': self.request.user.pk,
                           'rpk': self.object.response.resume.pk,
                           'pk': self.object.response.pk
                       })
