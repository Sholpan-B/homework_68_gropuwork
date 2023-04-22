from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import CustomUser
from job.managers import HHProjectManager
from job.models.base import BaseModel
from job.models.candidate import CategoryChoice, Resume


class Vacancy(BaseModel):
    created_by = models.ForeignKey(get_user_model(), verbose_name='Vacancy created by',
                                   related_name='vacancies', null=False, blank=False, on_delete=models.CASCADE)
    location = models.CharField(verbose_name='Company location', max_length=100, null=False, blank=False)
    position = models.CharField(max_length=100, null=False, blank=False)
    category = models.CharField(verbose_name='Job field', choices=CategoryChoice.choices, max_length=100)
    salary = models.IntegerField(verbose_name='Offered salary', null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    experience_from = models.IntegerField(null=False, blank=False, verbose_name='Expected experience from')
    experience_to = models.IntegerField(null=False, blank=False, verbose_name='Expected experience to')
    is_active = models.BooleanField(default=True, null=False)

    objects = HHProjectManager()

    def __str__(self):
        return f"{self.position}"

    class Meta:
        db_table = "vacancy"


class Response(models.Model):
    resume = models.ForeignKey(Resume, verbose_name='Resume', on_delete=models.CASCADE, related_name='response_resume')
    vacancy = models.ForeignKey(Vacancy, verbose_name='Vacancy', on_delete=models.CASCADE, related_name='response_vacancy')

    def __str__(self):
        return f"{self.resume} {self.vacancy}"

    class Meta:
        verbose_name = "Response"
        verbose_name_plural = "Responses"


class ResponseMessage(models.Model):
    response = models.ForeignKey(Response, verbose_name='Response to vacancy', on_delete=models.CASCADE,
                                 related_name='response_message')
    responded_by = models.ForeignKey(get_user_model(), related_name='messages', null=False, blank=False,
                                     on_delete=models.CASCADE)
    text = models.CharField(max_length=3000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
