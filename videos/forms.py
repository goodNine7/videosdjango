from django import forms
from .models import Channel

class EditChannelForm(forms.ModelForm):
    class Meta:
        model=Channel
        fields=('name', 'avatar', 'description')
        # widgets={
        #     'name':forms.TextInput(),
        #     'avatar':forms.FileInput(),
        #     'description':forms.Textarea()
        # }