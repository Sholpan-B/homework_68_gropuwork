from django.db import models
from django.db.models import QuerySet


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True


class CustomBaseQuerySet(QuerySet):
    def get_older(self):
        if hasattr(self.model, 'created_at'):
            return self.order_by('created_at').first()
        return self.first()
    