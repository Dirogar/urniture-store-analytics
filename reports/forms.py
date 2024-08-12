from django import forms
from django.forms import DateInput
from django.utils import timezone
from django.core.validators import ValidationError
from .models import Comment, Store


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


class StoreFilterForm(forms.Form):
    store = forms.MultipleChoiceField(
        choices=[],
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'size': 4})
    )

    def __init__(self, *args, **kwargs):
        accessible_stores = kwargs.pop('accessible_stores', None)
        super().__init__(*args, **kwargs)
        if accessible_stores:
            self.fields['store'].choices = [(store.id, store.name) for store in accessible_stores]


class CommentFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('В работе', 'В работе'),
        ('Не выполнено', 'Не выполнено'),
        ('Выполнено', 'Выполнено'),
        # Добавьте другие статусы по необходимости
    ]

    show_statuses = forms.MultipleChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Отображать комментарии со статусами"
    )




