from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.fields import ArrayField
from django.conf import settings 
from .managers import LabManager
from djrichtextfield.models import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify

class Lab(models.Model):
    """A typical class defining a model, derived from the Model class."""
    departments = [('AfricanAmericanStudies', 'African American Studies'), ('AfricanStudies', 'African Studies'), ('AmericanStudies', 'American Studies'), ('Anesthesiology', 'Anesthesiology'), ('Anthropology', 'Anthropology'), ('AppliedMathematics', 'Applied Mathematics'), ('AppliedPhysics', 'Applied Physics'), ('ArchaeologicalStudies', 'Archaeological Studies'), ('Architecture', 'Architecture'), ('Astronomy', 'Astronomy'), ('BiologicalBiomedicalSciences', 'Biological & Biomedical Sciences'), ('BiomedicalEngineering', 'Biomedical Engineering'), ('Biostatistics', 'Biostatistics'), ('CellBiology', 'Cell Biology'), ('CellularMolecularPhysiology', 'Cellular & Molecular Physiology'), ('ChemicalEnvironmentalEngineering', 'Chemical & Environmental Engineering'), ('Chemistry', 'Chemistry'), ('ChildStudyCenter', 'Child Study Center'), ('ChronicDiseaseEpidemiology', 'Chronic Disease Epidemiology'), ('Classics', 'Classics'), ('ComparativeLiterature', 'Comparative Literature'), ('ComparativeMedicine', 'Comparative Medicine'), ('ComputationalBiologyBioinformatics', 'Computational Biology & Bioinformatics'), ('ComputerScience', 'Computer Science'), ('Dermatology', 'Dermatology'), ('EarthPlanetarySciences', 'Earth & Planetary Sciences'), ('EastAsianLanguagesLiteratures', 'East Asian Languages & Literatures'), ('EastAsianStudies', 'East Asian Studies'), ('EcologyEvolutionaryBiology', 'Ecology & Evolutionary Biology'), ('Economics', 'Economics'), ('ElectricalEngineering', 'Electrical Engineering'), ('EmergencyMedicine', 'Emergency Medicine'), ('EngineeringAppliedScience', 'Engineering & Applied Science'), ('EnglishLanguageLiterature', 'English Language & Literature'), ('EnvironmentalHealthSciences', 'Environmental Health Sciences'), ('EpidemiologyofMicrobialDiseases', 'Epidemiology of Microbial Diseases'), ('EuropeanRussianStudies', 'European & Russian Studies'), ('ExperimentalPathology', 'Experimental Pathology'), ('FilmMediaStudies', 'Film & Media Studies'), ('ForestryEnvironmentalStudies', 'Forestry & Environmental Studies'), ('French', 'French'), ('Genetics', 'Genetics'), ('German', 'German'), ('GlobalAffairs', 'Global Affairs'), ('HealthCareManagement', 'Health Care Management'), ('HealthPolicyManagement', 'Health Policy & Management'), ('History', 'History'), ('HistoryofArt', 'History of Art'), ('HistoryofMedicine', 'History of Medicine'), ('HistoryofScienceMedicine', 'History of Science & Medicine'), ('Humanities', 'Humanities'), ('Immunobiology', 'Immunobiology'), ('InternalMedicine', 'Internal Medicine'), ('InternationalDevelopmentEconomics', 'International & Development Economics'), ('InvestigativeMedicine', 'Investigative Medicine'), ('ItalianStudies', 'Italian Studies'), ('JudaicStudies', 'Judaic Studies'), ('LaboratoryMedicine', 'Laboratory Medicine'), ('LatinAmericanStudies', 'Latin American Studies'), ('Law', 'Law'), ('Linguistics', 'Linguistics'), ('Management', 'Management'), ('Mathematics', 'Mathematics'), ('MechanicalEngineeringMaterialsScience', 'Mechanical Engineering & Materials Science'), ('MedievalStudies', 'Medieval Studies'), ('MicrobialPathogenesis', 'Microbial Pathogenesis'), ('Microbiology', 'Microbiology'), ('ModernMiddleEastStudies', 'Modern Middle East Studies'), ('MolecularBiophysicsBiochemistry', 'Molecular Biophysics & Biochemistry'), ('MolecularCellularDevelopmentalBiology', 'Molecular, Cellular & Developmental Biology'), ('Music', 'Music'), ('NearEasternLanguagesCivilizations', 'Near Eastern Languages & Civilizations'), ('Neurology', 'Neurology'), ('Neuroscience', 'Neuroscience'), ('NeuroscienceInterdepartmentalProgram', 'Neuroscience, Interdepartmental Program'), ('Neurosurgery', 'Neurosurgery'), ('Nursing', 'Nursing'), ('ObstetricsGynecologyReproductiveSciences', 'Obstetrics, Gynecology & Reproductive Sciences'), ('OphthalmologyVisualScience', 'Ophthalmology & Visual Science'), ('OrthopaedicsRehabilitation', 'Orthopaedics & Rehabilitation'), ('Pathology', 'Pathology'), ('Pediatrics', 'Pediatrics'), ('Pharmacology', 'Pharmacology'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('PoliticalScience', 'Political Science'), ('Psychiatry', 'Psychiatry'), ('Psychology', 'Psychology'), ('PublicHealth', 'Public Health'), ('RadiologyBiomedicalImaging', 'Radiology & Biomedical Imaging'), ('ReligiousStudies', 'Religious Studies'), ('RenaissanceStudies', 'Renaissance Studies'), ('SlavicLanguagesLiteratures', 'Slavic Languages & Literatures'), ('Sociology', 'Sociology'), ('SouthAsianStudies', 'South Asian Studies'), ('SpanishPortuguese', 'Spanish & Portuguese'), ('StatisticsDataScience', 'Statistics & Data Science'), ('Surgery', 'Surgery'), ('TheaterPerformanceStudies', 'Theater & Performance Studies'), ('TherapeuticRadiologyRadiationOncology', 'Therapeutic Radiology/Radiation Oncology'), ('Urology', 'Urology'), ('WomensGenderSexualityStudies', 'Women’s, Gender, & Sexuality Studies')]

    # Fields
    name = models.CharField(max_length=50)
    pi_name = models.CharField(max_length=255)
    pi_id = models.CharField(max_length=255)
    department = models.CharField(max_length=255, choices=departments)
    work_remote = models.BooleanField()
    work_in_person = models.BooleanField()
    accept_undergrads = models.BooleanField()
    accept_grads = models.BooleanField()
    email = models.CharField(max_length=255)
    website = models.CharField(max_length=255, blank=True)
    mentors = models.BooleanField()
    funded = models.BooleanField()
    project_desc = RichTextField(field_settings='advanced')
    search_vector = SearchVectorField(null=True, blank=True)
    objects = LabManager()
    edit = ArrayField(models.CharField(max_length=255, blank=True, null=True), default=list, blank=True, null=True)
    publications = ArrayField(models.TextField(blank=True, null=True), default=list, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, max_length=255)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

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
        self.slug = slugify(self.name)+ '-' + str(self.id)
        super().save(*args, **kwargs)

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of Lab."""
        return reverse('lab-detail', args=[self.slug])

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def __str__(self):
        """String for representing the Lab object (in Admin site etc.)."""
        return self.name
