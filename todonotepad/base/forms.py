from django.forms import ModelForm
from .models import Notepad

class NoteForm(ModelForm):
    class Meta:
        model = Notepad
        fields = ['title','body']
        