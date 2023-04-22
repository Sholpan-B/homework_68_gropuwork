from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextChoices

from accounts.models import CustomUser
from job.managers import HHProjectManager
from job.models.base import BaseModel


class CategoryChoice(TextChoices):
    MANAGEMENT = 'MANAGEMENT', 'MANAGEMENT'
    PROGRAMMING = 'PROGRAMMING ', 'PROGRAMMING '
    SALES = 'SALES', 'SALES'
    INSURANCE = 'INSURANCE ', 'INSURANCE '
    FINANCE = 'FINANCE', 'FINANCE'
    DESIGN = 'DESIGN', 'DESIGN'


class WorkExperience(BaseModel):
    company_name = models.CharField(verbose_name='Company name', max_length=100, null=False, blank=False)
    start_date = models.TextField(null=False, blank=False)
    end_date = models.TextField(null=False, blank=False)
    position = models.CharField(null=False, blank=False)
    responsibilities = models.TextField(null=False, blank=False)

    def __str__(self):
        return f'{self.company_name}'

    class Meta:
        db_table = "work_experience"


class Education(BaseModel):
    university = models.CharField(max_length=100, null=False, blank=False)
    start_date = models.TextField(verbose_name='Date of admission', null=False, blank=False)
    end_date = models.TextField(verbose_name='Graduation date', null=False, blank=False)
    major = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(verbose_name='City name', max_length=100, null=False, blank=False)

    def __str__(self):
        return f'{self.university}'

    class Meta:
        db_table = "education"


class Resume(BaseModel):
    title = models.CharField(verbose_name='Resume title', max_length=100, null=False, blank=False)
    created_by = models.ForeignKey(get_user_model(), verbose_name='Resume created by', related_name='resumes',
                                   null=False, blank=False, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False,blank=False)
    position = models.CharField(null=False, blank=False)
    category = models.CharField(verbose_name='Job field', choices=CategoryChoice.choices, max_length=100)
    salary = models.IntegerField(verbose_name='Expected salary', null=False, blank=False)
    telegram = models.URLField(verbose_name='Telegram', null=False, blank=False)
    email = models.EmailField(unique=False, null=False, blank=False,)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    work_experience = models.ManyToManyField(WorkExperience, related_name='worker_experience', blank=True)
    education = models.ManyToManyField(Education, related_name='worker_education', blank=True)
    is_active = models.BooleanField(default=True, null=False)

    objects = HHProjectManager()

    def __str__(self):
        return f"{self.first_name} {self.position}"

    class Meta:
        db_table = "resume"
