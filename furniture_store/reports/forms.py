from django import forms
from django.forms import DateInput
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'finish_planned_date']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'finish_planned_date': DateInput(
                format=('%Y-%m-%d'),
                attrs={
                       'type': 'date',
                       'placeholder': 'Select a date'}
            ),
        }

