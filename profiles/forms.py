from django import forms
from .models import UserProfile


class UsersProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
        '''
        Taken and altered from the Code Institutes
        walkthrough Project Boutique Ado
        '''
        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on first field
            """
            super().__init__(*args, **kwargs)
            placeholders = {
                'def_first_name': 'first_name',
                'def_last_name': 'last_name',
                'def_email': 'email',
                'def_phone': 'phone',
                'def_street': 'street',
                'def_town': 'town',
                'def_country': 'country',
            }

            self.fields['def_first_name'].widget.attrs['autofocus'] = True
            for field in self.fields:
                if field != 'default_country':
                    if self.fields[field].required:
                        placeholder = f'{placeholders[field]} *'
                    else:
                        placeholder = placeholders[field]
                    self.fields[field].widget.attrs['placeholder'] =
                    (placeholder)
                self.fields[field].widget.attrs['class'] =
                ('border-black rounded-0 profile-form-input')
                self.fields[field].label = False

