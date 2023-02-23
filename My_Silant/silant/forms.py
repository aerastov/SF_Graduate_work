from django import forms
from .models import *
import datetime

from django.utils import timezone
now = timezone.now()
print("now = ", now.year)

class FactoryNumber(forms.Form):
    factory_number = forms.CharField(label='Заводской номер:', max_length=20)


class CreateCarForm(forms.ModelForm):
    class Meta:
        model = Car
        widgets = {'factory_number': forms.Textarea(attrs={'rows': 1}), 'engine_number': forms.Textarea(attrs={'rows': 1}),
                   'transmission_number': forms.Textarea(attrs={'rows': 1}), 'drive_axle_number': forms.Textarea(attrs={'rows': 1}),
                   'steerable_axle_number': forms.Textarea(attrs={'rows': 1}), 'supply_contract': forms.Textarea(attrs={'rows': 1}),
                   'consignee': forms.Textarea(attrs={'rows': 1}), 'delivery_address': forms.Textarea(attrs={'rows': 1}),
                   'equipment': forms.Textarea(attrs={'rows': 1}), 'date_of_shipment_from_the_factory': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1)))) }
        fields = '__all__'
    #date_of_shipment_from_the_factory
    # def __init__(self, *args, **kwargs):
    #     super(CreateCarForm, self).__init__(*args, **kwargs)
    #     self.fields['title'].label = "Название публикации:"
    #     self.fields['text'].label = "Текст публикации:"
