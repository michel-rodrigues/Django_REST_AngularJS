from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    password_validation
    )


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # Verifica o login e a senha
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:

            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Esse usuário não existe")

            if not user.check_password(password):
                raise forms.ValidationError("Senha incorreta")

            if not user.is_active:
                raise forms.ValidationError("Esse usuário não está ativo")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    #email = forms.EmailField()
    email_confirm = forms.EmailField(label='Confirme o email')
    #password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email_confirm',
            'password',
        ]
        widgets = {
            'password': forms.PasswordInput,
        }

    # A ordem em 'fields' e nome desse método implicam no funcionamento da
    # validação. "clean_email" e "clean_email_confirm" resultam e
    # comportamentos diferentes
    #def clean_email_confirm(self):
    #    email = self.cleaned_data.get('email')
    #    email_confirm = self.cleaned_data.get('email_confirm')
    #    if email != email_confirm:
    #        raise forms.ValidationError("Os endereços de email não são iguais")
    #    email_qs = User.objects.get(email=email)
    #    if email_qs.exists():
    #        raise forms.ValidationError("Esse email já está registrado")
    #    return email


    # Também é possível sobreescrever o método clean
    #
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_confirm = self.cleaned_data.get('email_confirm')
        if email != email_confirm:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")

        return super(UserRegisterForm,self).clean(*args, **kwargs)

