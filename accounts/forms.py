from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove all default help texts and bullet messages completely
        for field_name, field in self.fields.items():
            field.help_text = None
            field.widget.attrs.update({
                'class': 'form-control',
                'style': 'border-radius: 10px; padding: 10px 14px; border: 1.5px solid #E2E8F0;'
            })

        self.fields['username'].widget.attrs.update({'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm your password'})
