from django import forms
from django.forms import ModelForm
from .models import Poll

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question', 'description']
        textarea = forms.Textarea(attrs={
                'class': 'py-2 h-12 px-6 border-2 border-gray-300 rounded-xl shadow-xl placeholder:font-bold focus:ring-blue-500 focus:border-blue-400 focus:shadow-blue-100 focus-visible:ring-0 focus-visible:outline-0',
            })
        widgets = {'vote': textarea}
        exclude = ['made_by']
        for field in model._meta.fields:
            # print(field)
            widgets[field.name] = textarea
