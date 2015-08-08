from django.db import models
import datetime
import uuid

gender_choices = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('N', 'N/A')
)

phase_choices = (
    ('newly_added', 'Newly Added'),
    ('brainstorming_completed', 'Brainstorming Completed'),
    ('grouping_enabled', 'Grouping Enabled'),
    ('rating_completed', 'Rating Completed')
)

page_main_url = "http://localhost:8000/welcome/"

class Participant(models.Model):
    id = models.CharField(primary_key=True, default=str(uuid.uuid4()),  editable=False, max_length=36)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_added = models.DateTimeField(default=datetime.datetime.now)

    gender = models.CharField(max_length=1, choices=gender_choices, default='N')
    age = models.IntegerField(blank=True, null=True)
    position = models.CharField(blank=True, null=True, max_length=100)
    type_experience = models.CharField(blank=True, max_length=100)
    years_experience = models.IntegerField(blank=True, null=True)

    password = models.CharField(blank=True, max_length=100, default="veryDifficultPassphrase")

    current_phase = models.CharField(max_length=50, choices=phase_choices, default='newly_added')

    email = models.EmailField(null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def user_url(self):
        return page_main_url + str(self.id) + "/"

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
    participant = models.ForeignKey(Participant)
    statement = models.ForeignKey(DistilledStatement)
    rating = models.IntegerField()


class StatementSorting(models.Model):
    participant = models.ForeignKey(Participant)
    statement = models.ForeignKey(DistilledStatement)
    order = models.IntegerField()


modules = (
    ('home', 'Home'),
    ('brainstorm', 'Brainstorm'),
    ('group', 'Group'),
    ('rate', 'Rate')
)


class ModuleHeading(models.Model):
    module_name = models.CharField(max_length=100, choices=modules)
    heading_content = models.TextField()

    def __str__(self):
        return self.module_name