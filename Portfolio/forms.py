from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class EmailUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white dark:bg-darkBg border border-zinc-300 dark:border-zinc-700 rounded-lg px-4 py-3 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-indigo-500 transition-colors',
            'placeholder': 'name@domain.com'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full bg-white dark:bg-darkBg border border-zinc-300 dark:border-zinc-700 rounded-lg px-4 py-3 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-indigo-500 transition-colors',
            'placeholder': 'name@domain.com'
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full bg-white dark:bg-darkBg border border-zinc-300 dark:border-zinc-700 rounded-lg px-4 py-3 text-zinc-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary dark:focus:ring-indigo-500 transition-colors',
            'placeholder': 'Enter your password'
        })
    )

    error_messages = {
        'invalid_login': 'Please enter a correct email and password.',
        'inactive': 'This account is inactive.',
    }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            self.user_cache = authenticate(username=user.username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            else:
                self.confirm_login_allowed(self.user_cache)

        return cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

    def get_user(self):
        return getattr(self, 'user_cache', None)
