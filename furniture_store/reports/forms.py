from django import forms
from django.forms import DateInput
from django.utils import timezone
from django.core.validators import ValidationError
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
                       'placeholder': 'Select a date',
                       'class': 'form-control'
                }
            ),
        }

    def clean_finish_planned_date(self):
        """Проверяет что в форму передана валидная дата"""
        finish_planned_date = self.cleaned_data.get('finish_planned_date')
        current_date = timezone.now()
        if finish_planned_date <= timezone.now():
            raise ValidationError(
                'Планируемая дата выполнения должна быть в будущем'
            )
        return finish_planned_date



