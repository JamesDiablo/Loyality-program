from django import forms
from .models import Card

class CardSearch_Form(forms.Form):
    """
    Form for searching cards.

    Attributes:
        query (CharField): A text field for entering search query.
    """
    query = forms.CharField(
        required=False, 
        label='', 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control w-100', 
                'placeholder': 'Введите серию, номер или любые другие данные карточки (дата формата yyyy-mm-dd)'
            }
        )
    )

class Generator_Form(forms.Form):
    """
    Form for generating new cards.

    Attributes:
        series (CharField): A text field for entering card series.
        count (IntegerField): An integer field for entering the number of cards to generate.
        start_date (DateField): A date field for entering the start date of the card's active period.
        end_date (DateField): A date field for entering the end date of the card's active period.
    """
    series = forms.CharField(
        label='', 
        min_length=1, 
        max_length=4, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder': 'Введите серию карты'
            }
        )
    )
    count = forms.IntegerField(
        label='', 
        min_value=1, 
        max_value=300, 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'type': 'number', 
                'placeholder': '1-300', 
                'min': '1', 
                'max': '300'
            }
        )
    )
    start_date = forms.DateField(
        label='', 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'type': 'date'
            }
        )
    )
    end_date = forms.DateField(
        label='', 
        required=True, 
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'type': 'date'
            }
        )
    )

    def clean(self):
        """
        Validate the form fields.

        Raises:
            ValidationError: If the start date is greater than or equal to the end date.
        """
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if start_date >= end_date:
            raise forms.ValidationError("Дата начала активности должна быть меньше, чем дата окончания действия карты")

        return cleaned_data
        
    def clean_series(self):
        """
        Validate the form field `series`.

        Raises:
            ValidationError: If the series isn't a chars or digits.
            ValidationError: If the card object with the entered series isn't in the database.
        """
        cleaned_data = super().clean()
        series = cleaned_data.get("series")

        if series.isalnum() == False:
            raise forms.ValidationError("В серии можно использовать только буквы и цифры")

        if Card.objects.filter(series=series).exists():
            raise forms.ValidationError("Карта с такой серией уже существует")
        
        return series