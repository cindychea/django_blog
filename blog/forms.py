from .models import Article
from django.forms import ModelForm
from django import forms
from django.core.validators import MinLengthValidator, ValidationError
from django.utils import timezone
import datetime

class ArticleForm(ModelForm):

    title = forms.CharField(max_length=255)
    body = forms.CharField(validators=[MinLengthValidator(1)], widget=forms.Textarea)
    # where would the message from the min legnth validator show up [MinLengthValidator(4)]
    draft = forms.BooleanField()
    published_date = forms.DateField()

    class Meta:
        model = Article
        fields = ['title', 'body', 'draft', 'published_date']
    
    def clean(self):
        form = super().clean()
        draft = form.get('draft')
        published_date = form.get('published_date')
        present = datetime.date.today()
        if draft and published_date < present:
            raise ValidationError('Invalid publish date, must be future date.')
        elif draft is False and published_date > present:
            raise ValidationError('Invalid publish date, must be past date.')

    # where would the validation error show up
        