# forms.py
from django import forms
from .models import *


class JSONFileUploadForm(forms.Form):
    # json_file = forms.FileField()

    json_file= forms.FileField(max_length=100,widget=forms.FileInput(attrs={
        "id":"name",
        "type":"file",
        "name":"name",
        "class":"w-full mt-1 rounded border-gray-100/50 placeholder:text-sm placeholder:text-gray-400 dark:bg-transparent dark:border-gray-800 focus:ring-0 focus:ring-offset-0 dark:text-gray-200",

        }
    ))



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""