from django.urls import path

from job.views.education import CreateEducationView, EditEducationView, DeleteEducationView
from job.views.experience import CreateExperienceView, EditExperienceView, DeleteExperienceView
from job.views.index import IndexView
from job.views.response import ResponseListView, ResponseView, AddResponseMessageView, DeleteResponseMessageView
from job.views.resume import CreateResumeView, ListResumesView, ResumeView, EditResumeView, DeleteResumeView
from job.views.vacancy import CreateVacancyView, ListVacancyView, VacancyView, EditVacancyView, DeleteVacancyView

app_name = 'job'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('', IndexView.as_view(), name='home'),

    path('user/<int:pk>/resumes/create/', CreateResumeView.as_view(), name='create_resume'),
    path('user/<int:pk>/resumes/', ListResumesView.as_view(), name='resumes'),
    path('user/<int:upk>/resumes/<int:pk>/', ResumeView.as_view(), name='resume'),
    path('user/<int:upk>/resumes/<int:pk>/edit/', EditResumeView.as_view(), name='edit_resume'),
    path('user/<int:upk>/resumes/<int:pk>/delete/', DeleteResumeView.as_view(), name='delete_resume'),

    path('user/<int:upk>/vacancy/create/', CreateVacancyView.as_view(), name='create_vacancy'),
    path('user/<int:pk>/vacancies/', ListVacancyView.as_view(), name='vacancies'),
    path('user/<int:upk>/vacancies/<int:pk>/', VacancyView.as_view(), name='vacancy'),
    path('user/<int:upk>/vacancies/<int:pk>/edit/', EditVacancyView.as_view(), name='edit_vacancy'),
    path('user/<int:upk>/vacancies/<int:pk>/delete/', DeleteVacancyView.as_view(), name='delete_vacancy'),

    path('user/<int:pk>/responses/', ResponseListView.as_view(), name='responses'),
    path('user/<int:upk>/resumes/<int:rpk>/response/<int:pk>/', ResponseView.as_view(), name='response'),
    path('user/<int:upk>/resumes/<int:rpk>/response/<int:pk>/add-message/',
         AddResponseMessageView.as_view(),
         name='add_response_message'),
    path('user/<int:upk>/responds/<int:rpk>/response-message/<int:pk>/delete/',
         DeleteResponseMessageView.as_view(),
         name='delete_response_message'),

    path('user/<int:upk>/resumes/<int:pk>/educations/create/', CreateEducationView.as_view(),
         name='create_education'),
    path('user/<int:upk>/resumes/<int:rpk>/educations/<int:pk>/edit/', EditEducationView.as_view(),
         name='edit_education'),
    path('user/<int:upk>/resumes/<int:rpk>/educations/<int:pk>/delete/', DeleteEducationView.as_view(),
         name='delete_education'),

    path('user/<int:upk>/resumes/<int:pk>/experiences/create/', CreateExperienceView.as_view(),
         name='create_experience'),
    path('user/<int:upk>/resumes/<int:rpk>/experiences/<int:pk>/edit/', EditExperienceView.as_view(),
         name='edit_experience'),
    path('user/<int:upk>/resume/<int:rpk>/experiences/<int:pk>/delete/', DeleteExperienceView.as_view(),
         name='delete_experience'),

]
