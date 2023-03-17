from django import forms
from django.contrib.auth.models import User


class UpdateAccountForm(forms.ModelForm):
    # LIST=(("client", "Клиент"), ("service", "Сервисная организация"), ("manager", "Менеджер"), ("admin", "Администратор"))
    # group = forms.ChoiceField(choices=LIST, widget=forms.Select, label = "Роль (группа)", help_text='Группа, к которой '
    #                                     'принадлежит данный пользователь. Пользователь получит все права, указанные в '
    #                                     'группе. Тонкую настройку прав самой группы вы можете сделать в административной'
    #                                     ' части сайта (/admin).')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'groups', 'is_superuser', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].help_text='Обязательное поле. Введите ваше имя или название компании'
        self.fields['first_name'].required=True
        self.fields['username'].label='Логин'
        self.fields['groups'].help_text='Группа, к которой принадлежит данный пользователь. Пользователь получит все ' \
                                        'права, указанные в группе. Тонкую настройку прав самой группы вы можете сделать ' \
                                        'в административной части сайта (/admin).'
        self.fields['groups'].label='Роль (группа)'


class CreateAccountForm(forms.ModelForm):
    # service_company = forms.CharField(max_length=200, help_text='Use puns liberally', label = "Сервисная компания")
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'email', 'groups', 'is_superuser', 'is_staff', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].help_text='Обязательное поле. Введите ваше имя или название компании'
        self.fields['first_name'].required=True
        self.fields['username'].label='Логин'
        self.fields['groups'].help_text='Группа, к которой принадлежит данный пользователь. Пожалуйста выберите только ' \
                                        'одну из групп. Пользователь получит все права, указанные в группе. Тонкую ' \
                                        'настройку прав самой группы вы можете сделать в административной части сайта ' \
                                        '(/admin).'
        self.fields['groups'].label='Роль (группа)'