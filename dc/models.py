from django.db import models
import datetime
import uuid

from django.template.loader import get_template

from django.template import Context

from django.utils.crypto import get_random_string

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', "Don't want to answer")
)

main_discipline_choices = (
    ('health', 'Health'),
    ('economy', 'Economy/finance'),
    ('sociology', 'Sociology/social work'),
    ('law', 'Policy and Law'),
    ('other', 'Other')
)

phase_choices = (
    ('newly_added', 'Newly Added'),
    ('brainstorming_completed', 'Brainstorming Completed'),
    ('grouping_enabled', 'Grouping Enabled'),
    ('rating_completed', 'Rating Completed')
)


page_main_url = "http://qba.pythonanywhere.com/"


class Participant(models.Model):
    id = models.CharField(primary_key=True, default=str(uuid.uuid4()), unique=True, editable=False, blank=True, max_length=36)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.datetime.now)

    gender = models.CharField(max_length=1, choices=gender_choices, default='N')
    age = models.IntegerField(default=0)
    age.max_value=150

    position = models.CharField(max_length=100)

    type_experience = models.CharField(max_length=100, blank=True)
    type_experience.verbose_name = "Area of expertise related to exploitation " \
                                   "(for example: precarious, vulnerable, unfree, low-paid or migrant work; " \
                                   "forced labour, modern slavery or human trafficking, ...)"

    discipline = models.CharField(max_length=100, choices=main_discipline_choices, default='other')
    discipline.verbose_name = "Main discipline of expertise"

    other_discipline = models.CharField(max_length=100, blank=True)
    other_discipline.verbose_name = "If Other, please specify:..."

    institution = models.CharField(max_length=100, blank=True)
    institution.verbose_name = "Institution or Organisation"

    country = models.CharField(max_length=200, blank=True)
    country.verbose_name = "Country"

    years_experience = models.IntegerField(blank=True)
    years_experience.verbose_name= "Years of experience in the field related to ‘exploitation’"

    password = models.CharField(max_length=100, default=get_random_string(length=6))

    current_phase = models.CharField(max_length=50, choices=phase_choices, default='newly_added')

    email = models.EmailField()

    def __str__(self):
        return self.full_name()

    def __unicode__(self):
        return self.full_name()

    def user_url(self):
        return page_main_url + "welcome/" + str(self.id) + "/"

    def full_name(self):
        return self.first_name + " " + self.last_name

    user_url.short_description = "User URL"

class ParticipantStatement(models.Model):
    author = models.ForeignKey(Participant)
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    text = models.TextField()

    def __str__(self):
        return self.text

class DistilledStatement(models.Model):
    text_question = models.TextField()

    def __str__(self):
        return self.text_question


class StatementRating(models.Model):
    author = models.ForeignKey(Participant)
    statement = models.ForeignKey(DistilledStatement)
    rating = models.IntegerField()


class StatementSorting(models.Model):
    author = models.ForeignKey(Participant)
    statement = models.ForeignKey(DistilledStatement)
    order = models.IntegerField()
    group_name = models.TextField()


modules = (
    ('home', 'Home'),
    ('brainstorm', 'Brainstorm'),
    ('group', 'Group'),
    ('rate', 'Rate'),
    ('user_email_template', "User Email Template")

)


class ModuleHeading(models.Model):
    module_name = models.CharField(max_length=100, choices=modules)
    heading_content = models.TextField()

    def __str__(self):
        return self.module_name