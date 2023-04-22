from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView

from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        next_url = request.GET.get('next')
        form_data = {} if not next_url else {'next': next_url}
        form = self.form(form_data)
        context = {'login_form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('accounts:login')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        next_url = form.cleaned_data.get('next')
        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "User not found")
            return redirect('accounts:login')
        login(request, user)
        messages.success(request, 'Welcome!')
        if next_url:
            return redirect(next_url)
        return redirect('job:index')


def logout_view(request):
    logout(request)
    return redirect('job:index')


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            user.groups.add('employer' if user.role == 'EMPLOYER' else 'candidate')
            user.set_password(form.cleaned_data.get('password'))

            login(request, user)
            return redirect(reverse('job:index'))
        context = {}
        context['form'] = form
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        kwargs['form'] = UserChangeForm(instance=self.get_object())
        return super().get_context_data(**kwargs)

    def get_object(self, queryset=None):
        return get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))


class UserChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'profile.html'
    context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
