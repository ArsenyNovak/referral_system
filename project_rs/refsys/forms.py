from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

from refsys.models import ClientUser


class NumberForm(forms.Form):
    number = forms.CharField(label = 'Введите номер телефона:  ')

    def clean_number(self):
        data = self.cleaned_data['number']
        if not data.isdigit():
            raise forms.ValidationError("Номер должен состоять только из цифр (375331234567).")
        if len(data) < 10:
            raise forms.ValidationError("В номере телефона должно быть не менее 10 цифр.")
        return data


class CheckNumberForm(forms.Form):
    number = forms.CharField(label='номер телефона:  ')
    code = forms.CharField(label='Код:  ', max_length=4)

    def clean_number(self):
        data = self.cleaned_data['number']
        if not data.isdigit():
            raise forms.ValidationError("Номер должен состоять только из цифр (375331234567).")
        if len(data) < 10:
            raise forms.ValidationError("В номере телефона должно быть не менее 10 цифр.")
        return data


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='номер телефона')
    invite_code = forms.CharField(disabled=True, label='инвайт-код')

    class Meta:
        model = get_user_model()
        fields = ['username', 'invite_code', 'other_code']
        labels = {
            'other_code': "приглашённый инвайт-код "
        }

    def clean_other_code(self):
        data = self.cleaned_data['other_code']
        my_invite = self.cleaned_data['invite_code']
        if not ClientUser.objects.filter(invite_code=data).exclude(invite_code=my_invite).exists():
            raise forms.ValidationError("нет пользователя с таким инвайт-кодом")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        value = None
        if self.instance and getattr(self.instance, 'other_code', None):
            value = getattr(self.instance, 'other_code')
        elif 'username' in self.initial:
            value = self.initial['other_code']
        if value:
            self.fields['other_code'].widget.attrs['disabled'] = 'disabled'
    #
    #

