from urllib.parse import urlencode

from django.db.models import Q
from django.views.generic import ListView

from job.forms.search import SearchForm
from job.models import Vacancy, Resume


class IndexView(ListView):
    template_name = 'vacancies/vacancies_list.html'
    model = Vacancy
    ordering = ('-updated_at',)
    context_object_name = 'vacancies'
    paginate_by = 20
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        self.search_value_resume = self.get_search_value()
        self.category = request.GET.get('category')
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(position__icontains=self.search_value)
            queryset = queryset.filter(query).order_by('-salary')
        if self.category:
            queryset = Vacancy.objects.filter(Q(category__icontains=self.category)).order_by('-salary')
            if self.request.user.role == 'company':
                queryset = Resume.objects.filter(Q(category__icontains=self.category)).order_by('-salary')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        if not self.category:
            self.category = ""
        context = super(IndexView, self).get_context_data(object_list=object_list, **kwargs)
        context['resumes'] = Resume.objects.filter(Q(category__icontains=self.category)).order_by('-salary')
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context
