from django.forms import ModelForm
from .models import Poll

class PollForm(ModelForm):
    class Meta:
        model = Poll
        fields = '__all__'