from django import forms

from . import models

from django.forms import formsets


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        #fields = '__all__' #TODO fix

        fields = [
            'first_name',
            'last_name',
            'gender',
            'age',
            'institution',
            'position',
            'discipline',
            'type_experience',
            'years_experience'
        ]

        widgets = {
            'years_experience': forms.NumberInput(attrs={'min': 0, 'max': 99} ),
            'age': forms.NumberInput(attrs={'min': 18, 'max': 99} ),
        }


class ParticipantStatementForm(forms.Form):
    text = forms.TextInput()


ParticipantStatementFormSet = formsets.formset_factory(ParticipantStatementForm)
