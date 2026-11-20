from django import forms


class DestinationImageForm(forms.Form):
    image = forms.ImageField(required=False)
