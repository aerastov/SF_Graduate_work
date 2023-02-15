from django import forms

class FactoryNumber(forms.Form):
    factory_number = forms.CharField(label='Заводской номер', max_length=100)