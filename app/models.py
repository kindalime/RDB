from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from .managers import LabManager

class Lab(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # TODO: get department choices and program in here
    departments = [("abbreviated", "actual")]

    # Fields
    name = models.CharField(help_text="", max_length=255)
    pi_name = models.CharField(help_text="", max_length=255)
    pi_id = models.CharField(help_text="", max_length=255)
    department = models.CharField(help_text="", max_length=255, choices=departments)
    work_remote = models.BooleanField(help_text="")
    work_in_person = models.BooleanField(help_text="")
    accept_undergrads = models.BooleanField(help_text="")
    accept_grads = models.BooleanField(help_text="")
    email = models.CharField(help_text="", max_length=255)
    website = models.CharField(help_text="", max_length=255)
    mentors = models.BooleanField(help_text="")
    funded = models.BooleanField(help_text="")
    project_desc = models.TextField(help_text="")
    search_vector = SearchVectorField(null=True, blank=True)
    objects = LabManager()

    # Metadata
    class Meta:
        ordering = ['-name']

    def save(self, *args, **kwargs):
        super(Lab, self).save(*args, **kwargs)
        self.search_vector = (
            SearchVector('name', weight='A')
            + SearchVector('project_desc', weight='B')
            + SearchVector('pi_name', weight='C')
            + SearchVector('email', weight='D')
        )
        super().save(*args, **kwargs)

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Lab."""
        return reverse('lab-detail', args=[str(self.id)])

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        """String for representing the Lab object (in Admin site etc.)."""
        return self.name
