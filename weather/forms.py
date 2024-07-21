from django import forms
from weather.models import History


class ForecastForm(forms.Form):
    CHOICES = [
        (1, 'на 1 день'),
        (2, 'на 2 дня'),
        (3, 'на 3 дня'),
        (4, 'на 4 дня'),
        (5, 'на 5 дней'),
        (6, 'на 6 дней'),
        (7, 'на 7 дней')
    ]

    city = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
        'class': 'form-control top-spacing-input',
        'id': 'select_city',
        'placeholder': 'Введите город...',
        'title': 'Введите город в это поле.',
        'data-api-key': 'ebf5f41483211937312a3638eccb7f9a5c26b89c'
        }),
        required=False,
        label=""
    )

    history = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control',
            'title': 'Выберите город',
        }),
        required=False,
        label="Недавно просмотренные города"
    )

    days = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control top-spacing-input',
            'id': 'select_days',
            'title': 'Выберите количество дней',
        }),
        choices=CHOICES,
        required=True,
        label=""
    )

    def __init__(self, request, *args, **kwargs):
        super(ForecastForm, self).__init__(*args, **kwargs)

        queryset = History.objects.filter(user=request.user.id).order_by('-created_at')

        if queryset:
            if len(queryset) > 10:
                queryset = queryset[:10]
            history = set()
            for item in queryset:
                history.add((item.city, item.city))
            self.fields['history'].choices = sorted(history)
        else:
            self.fields['history'].widget = forms.HiddenInput()
