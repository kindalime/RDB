from django.db import models
from django.urls import reverse
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.fields import ArrayField
from django.conf import settings 
from .managers import LabManager

from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class Lab(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # TODO: get department choices and program in here
    departments = [("CellBiology", "Cell Biology"),
                    ("ComputationalBiologyBioinformatics", "Computational Biology & Bioinformatics"),
                    ("EcologyEvolutionaryBiology", "Ecology & Evolutionary Biology"),
                    ("ForestryEnvironmentalStudies", "Forestry & Environmental Studies"),
                    ("Microbiology", "Microbiology"),
                    ("MolecularCellularDevelopmentalBiology", "Molecular, Cellular & Developmental Biology"),
                    ("BiologicalBiomedicalSciences", "Biological & Biomedical Sciences"),
                    ("CellularMolecularPhysiology", "Cellular & Molecular Physiology"),
                    ("MolecularBiophysicsBiochemistry", "Molecular Biophysics & Biochemistry"),
                    ("Neuroscience", "Neuroscience"),
                    ("NeuroscienceInterdepartmentalProgram", "Neuroscience, Interdepartmental Program"),
                    ("BiomedicalEngineering", "Biomedical Engineering"),
                    ("ChemicalEnvironmentalEngineering", "Chemical & Environmental Engineering"),
                    ("ComputerScience", "Computer Science"),
                    ("ElectricalEngineering", "Electrical Engineering"),
                    ("EngineeringAppliedScience", "Engineering & Applied Science"),
                    ("MechanicalEngineeringMaterialsScience", "Mechanical Engineering & Materials Science"),
                    ("Biostatistics", "Biostatistics"),
                    ("HistoryofMedicine", "History of Medicine"),
                    ("Anesthesiology", "Anesthesiology"),
                    ("ChildStudyCenter", "Child Study Center"),
                    ("ChronicDiseaseEpidemiology", "Chronic Disease Epidemiology"),
                    ("ComparativeMedicine", "Comparative Medicine"),
                    ("Dermatology", "Dermatology"),
                    ("EmergencyMedicine", "Emergency Medicine"),
                    ("EnvironmentalHealthSciences", "Environmental Health Sciences"),
                    ("EpidemiologyofMicrobialDiseases", "Epidemiology of Microbial Diseases"),
                    ("ExperimentalPathology", "Experimental Pathology"),
                    ("Genetics", "Genetics"),
                    ("HealthCareManagement", "Health Care Management"),
                    ("HealthPolicyManagement", "Health Policy & Management"),
                    ("Immunobiology", "Immunobiology"),
                    ("InternalMedicine", "Internal Medicine"),
                    ("InvestigativeMedicine", "Investigative Medicine"),
                    ("LaboratoryMedicine", "Laboratory Medicine"),
                    ("MicrobialPathogenesis", "Microbial Pathogenesis"),
                    ("Neurology", "Neurology"),
                    ("Neurosurgery", "Neurosurgery"),
                    ("Nursing", "Nursing"),
                    ("ObstetricsGynecologyReproductiveSciences", "Obstetrics, Gynecology & Reproductive Sciences"),
                    ("OphthalmologyVisualScience", "Ophthalmology & Visual Science"),
                    ("OrthopaedicsRehabilitation", "Orthopaedics & Rehabilitation"),
                    ("Pathology", "Pathology"),
                    ("Pediatrics", "Pediatrics"),
                    ("Pharmacology", "Pharmacology"),
                    ("Psychiatry", "Psychiatry"),
                    ("PublicHealth", "Public Health"),
                    ("RadiologyBiomedicalImaging", "Radiology & Biomedical Imaging"),
                    ("Surgery", "Surgery"),
                    ("TherapeuticRadiologyRadiationOncology", "Therapeutic Radiology/Radiation Oncology"),
                    ("Urology", "Urology"),
                    ("AfricanStudies", "African Studies"),
                    ("AmericanStudies", "American Studies"),
                    ("Architecture", "Architecture"),
                    ("Classics", "Classics"),
                    ("ComparativeLiterature", "Comparative Literature"),
                    ("EastAsianLanguagesLiteratures", "East Asian Languages & Literatures"),
                    ("EnglishLanguageLiterature", "English Language & Literature"),
                    ("FilmMediaStudies", "Film & Media Studies"),
                    ("French", "French"),
                    ("German", "German"),
                    ("History", "History"),
                    ("HistoryofArt", "History of Art"),
                    ("HistoryofScienceMedicine", "History of Science & Medicine"),
                    ("Humanities", "Humanities"),
                    ("ItalianStudies", "Italian Studies"),
                    ("JudaicStudies", "Judaic Studies"),
                    ("MedievalStudies", "Medieval Studies"),
                    ("Music", "Music"),
                    ("NearEasternLanguagesCivilizations", "Near Eastern Languages & Civilizations"),
                    ("Philosophy", "Philosophy"),
                    ("ReligiousStudies", "Religious Studies"),
                    ("RenaissanceStudies", "Renaissance Studies"),
                    ("SlavicLanguagesLiteratures", "Slavic Languages & Literatures"),
                    ("SpanishPortuguese", "Spanish & Portuguese"),
                    ("TheaterPerformanceStudies", "Theater & Performance Studies"),
                    ("AppliedMathematics", "Applied Mathematics"),
                    ("AppliedPhysics", "Applied Physics"),
                    ("Astronomy", "Astronomy"),
                    ("Chemistry", "Chemistry"),
                    ("EarthPlanetarySciences", "Earth & Planetary Sciences"),
                    ("Mathematics", "Mathematics"),
                    ("Physics", "Physics"),
                    ("AfricanAmericanStudies", "African American Studies"),
                    ("Anthropology", "Anthropology"),
                    ("ArchaeologicalStudies", "Archaeological Studies"),
                    ("EastAsianStudies", "East Asian Studies"),
                    ("Economics", "Economics"),
                    ("EuropeanRussianStudies", "European & Russian Studies"),
                    ("GlobalAffairs", "Global Affairs"),
                    ("InternationalDevelopmentEconomics", "International & Development Economics"),
                    ("LatinAmericanStudies", "Latin American Studies"),
                    ("Law", "Law"),
                    ("Linguistics", "Linguistics"),
                    ("Management", "Management"),
                    ("ModernMiddleEastStudies", "Modern Middle East Studies"),
                    ("PoliticalScience", "Political Science"),
                    ("Psychology", "Psychology"),
                    ("Sociology", "Sociology"),
                    ("SouthAsianStudies", "South Asian Studies"),
                    ("StatisticsDataScience", "Statistics & Data Science"),
                    ("WomensGenderSexualityStudies", "Women’s, Gender, & Sexuality Studies")]

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
    project_desc = models.TextField()
    search_vector = SearchVectorField(null=True, blank=True)
    objects = LabManager()
    edit = ArrayField(models.CharField(max_length=255, blank=True, null=True), default=list, blank=True, null=True)
    publications = ArrayField(models.TextField(blank=True, null=True), default=list, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

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
