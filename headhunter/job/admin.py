from django.contrib import admin

from job.models import Vacancy, Resume, Education, WorkExperience, Response

admin.site.register(Vacancy)
admin.site.register(Resume)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(Response)
