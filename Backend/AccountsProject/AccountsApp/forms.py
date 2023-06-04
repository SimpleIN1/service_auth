from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from AccountsApp.services.user_view import send_login_detail, generate_password, send_email_directors


class UserPasswordNorRequiredCreationForm(UserCreationForm):
    select_action_password = forms.ChoiceField(
        choices=((1, 'Ввод пароля'), (2, 'Генерация пароля (Отправляется на почту)'), (3, 'Без ввода пароля')),
        label=_('Действия с паролем')
    )
    send_password = forms.BooleanField(
        label=_('Отправить пароль на почту'),
        required=False,
        help_text=_("Отправляется пароль, заполенный в ручную, на указанный электронный адрес.")
    )
    send_gen_password = forms.BooleanField(
        label=_('Отправить сгенерированный пароль на почту'),
        required=False,
        help_text=_("Отправляется сгенерированный пароль на указанный электронный адрес.")
    )
    open_access = forms.BooleanField(
        label=_('Открыть доступ'),
        required=False,
        help_text=_("пользователь получает доступ для использования системы.")
    )

    send_email_to_director = forms.BooleanField(
        label=_('Отправить письмо директору'),
        required=False,
        help_text=_(
            'Отправляется директор(у/ам) письмо, информирующее о том, что пользователь прошел регистрацию, с данными о пользователе.'
        ),
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False,
    )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        select_action_password = self.cleaned_data.get('select_action_password')
        if not select_action_password or int(select_action_password) == 1:
            if not password1 or password1 == '':
                self.add_error("password1", 'Обязательное поле')
            if not password2 or password2 == '':
                self.add_error("password2", 'Обязательное поле')
        self._validate_unique = True
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_added_admin_panel = True

        password = None
        type_user = self.cleaned_data.get('type_user')

        if 0 < type_user < 3:
            action_pass = int(self.cleaned_data.get('select_action_password'))
            # print(action_pass)

            if 0 < action_pass < 3:
                if action_pass == 1:
                    password = self.cleaned_data.get("password1")
                elif action_pass == 2:
                    password = generate_password()
                user.set_password(password)

                if self.cleaned_data.get('send_password'):
                    send_login_detail(user.email, password)
                elif self.cleaned_data.get('send_gen_password'):
                    send_login_detail(user.email, password)

            if self.cleaned_data.get('type_user') == 2 \
                    and self.cleaned_data.get('send_email_to_director'):
                send_email_directors(user)

            if self.cleaned_data.get('open_access'):
                user.is_verify = True
                user.is_active = True
            else:
                user.is_verify = False
                user.is_active = False

        if commit:
            user.save()
        return user
