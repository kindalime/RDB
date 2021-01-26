from django.db import models

class Lab(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # TODO: get department choices and program in here
    departments = [("abbreviated", "actual")]

    # Fields
    name = models.CharField(help_text="", max_length=255)
    pi_name = models.CharField(help_text="", max_length=255)
    pi_id = models.CharField(help_text="", max_length=255)
    department = models.CharField(help_text="", max_length=255, choices=departments) # cat 
    work_remote = models.BooleanField(help_text="")
    work_in_person = models.BooleanField(help_text="")
    keywords = models.JSONField(help_text="", null=True, blank=True) # list of keywords in JSON format
    accept_undergrads = models.BooleanField(help_text="")
    accept_grads = models.BooleanField(help_text="")
    email = models.CharField(help_text="", max_length=255)
    website = models.CharField(help_text="", max_length=255)
    mentors = models.BooleanField(help_text="")
    funded = models.BooleanField(help_text="")
    project_desc = models.TextField(help_text="")

    # Metadata
    class Meta:
        ordering = ['-name']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
