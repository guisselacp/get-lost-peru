from .models import DropMeALine
from django import forms


class DropForm(forms.ModelForm):
    class Meta:
        model = DropMeALine
        fields = ('name', 'email', 'message')