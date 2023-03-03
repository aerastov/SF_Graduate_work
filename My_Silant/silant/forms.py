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
        widgets = {'factory_number': forms.Textarea(attrs={'rows': 1}),
                   'engine_number': forms.Textarea(attrs={'rows': 1}),
                   'transmission_number': forms.Textarea(attrs={'rows': 1}),
                   'drive_axle_number': forms.Textarea(attrs={'rows': 1}),
                   'steerable_axle_number': forms.Textarea(attrs={'rows': 1}),
                   'supply_contract': forms.Textarea(attrs={'rows': 1}),
                   'consignee': forms.Textarea(attrs={'rows': 1}),
                   'delivery_address': forms.Textarea(attrs={'rows': 1}),
                   'equipment': forms.Textarea(attrs={'rows': 1}),
                   'date_of_shipment_from_the_factory': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1)))) }
        fields = '__all__'


class CreateMaintenancesForm(forms.ModelForm):
    # service_company = forms.CharField(max_length=200, help_text='Use puns liberally', label = "Сервисная компания")
    class Meta:
        model = Maintenance
        exclude = ('car',)
        widgets = {'order': forms.Textarea(attrs={'rows': 1}),
                   'maintenance_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   }

    def __init__(self, *args, **kwargs):
        service_company = kwargs.pop('initial')['service_company']
        super(CreateMaintenancesForm, self).__init__(*args, **kwargs)
        self.fields['service_company'].initial = service_company
        self.fields['service_company'].help_text='Назначить или изменить организацию может менеджер в информации о машине'
        self.fields['service_company'].widget.attrs['disabled'] = True


