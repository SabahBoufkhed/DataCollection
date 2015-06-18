from django.forms import ModelForm, Form
from django import forms

from . import models

from django.forms import formsets


class ParticipantForm(ModelForm):
    class Meta:
        model = models.Participant
        #fields = '__all__' #TODO fix

        fields = ['first_name', 'last_name', 'gender', 'age', 'position', 'type_experience']
        #
        # labels = {
        #     'name': _('Writer'),
        #     }
        # help_texts = {
        #     'name': _('Some useful help text.'),
        #     }
        # error_messages = {
        #     'name': {



class ParticipantStatementForm(forms.Form):
    text = forms.TextInput()


ParticipantStatementFormSet = formsets.formset_factory(ParticipantStatementForm)
