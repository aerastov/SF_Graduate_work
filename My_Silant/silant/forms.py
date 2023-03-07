from django import forms
from .models import *
import datetime

from django.utils import timezone
now = timezone.now()
# print("now = ", now.year)

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
        # exclude = ('car',)
        fields = '__all__'
        widgets = {'order': forms.Textarea(attrs={'rows': 1}),
                   'maintenance_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'order_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'car': forms.HiddenInput(),
                   }


    def __init__(self, *args, **kwargs):
        super(CreateMaintenancesForm, self).__init__(*args, **kwargs)
        service_company = kwargs.pop('initial')['service_company']
        # self.fields['service_company'].initial = service_company
        self.fields['service_company'].help_text='Назначить или изменить организацию для данной машины может менеджер в информации о машине'
        # self.fields['service_company'].widget.attrs['disabled'] = True
        self.fields['service_company'].widget.attrs['readonly'] = True

class UpdateMaintenancesForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets = {'order': forms.Textarea(attrs={'rows': 1}),
                   'maintenance_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'order_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'car': forms.HiddenInput(),
                   }


class CreateComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = '__all__'
        widgets = {'date_of_refusal': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'failure_node': forms.Textarea(attrs={'rows': 1}),
                   'parts_used': forms.Textarea(attrs={'rows': 1}),
                   'date_of_restoration': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'equipment_downtime': forms.Textarea(attrs={'rows': 1}),
                   'car': forms.HiddenInput(),
                   }


    def __init__(self, *args, **kwargs):
        super(CreateComplaintsForm, self).__init__(*args, **kwargs)
        self.fields['service_company'].help_text='Назначить или изменить организацию для данной машины может менеджер в информации о машине'



class UpdateComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = '__all__'
        widgets = {'date_of_refusal': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'failure_node': forms.Textarea(attrs={'rows': 1}),
                   'parts_used': forms.Textarea(attrs={'rows': 1}),
                   'date_of_restoration': forms.SelectDateWidget(years=list(reversed(range(2000, now.year + 1)))),
                   'equipment_downtime': forms.Textarea(attrs={'rows': 1}),
                   'car': forms.HiddenInput(),
                   }


class UpdateTechniqueModelForm(forms.ModelForm):
    class Meta:
        model = Technique_model
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateEngineModelForm(forms.ModelForm):
    class Meta:
        model = Engine_model
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateTransmissionModelForm(forms.ModelForm):
    class Meta:
        model = Transmission_model
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateDriveAxleModelForm(forms.ModelForm):
    class Meta:
        model = Drive_axle_model
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateSteerableAxleModelForm(forms.ModelForm):
    class Meta:
        model = Steerable_axle_model
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class CreateServiceCompanyForm(forms.ModelForm):
    class Meta:
        model = Service_company
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateServiceCompanyForm(forms.ModelForm):
    class Meta:
        model = Service_company
        exclude = ('user',)
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateTypeMaintenanceForm(forms.ModelForm):
    class Meta:
        model = Type_maintenance
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateDescriptionFailureForm(forms.ModelForm):
    class Meta:
        model = Description_failure
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}


class UpdateRecoveryMethodForm(forms.ModelForm):
    class Meta:
        model = Recovery_method
        fields = '__all__'
        widgets = {'name': forms.Textarea(attrs={'rows': 1}),}



