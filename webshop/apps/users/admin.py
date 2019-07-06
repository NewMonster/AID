from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label='密码确认')

    class Meta:
        model = User
        fields = ('username', 'password',)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('密码不正确')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': (
            'ch_name', 'gender',
        )}),
        ('权限', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )}),
        ('系统记录', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = (
        'username', 'gender', 'ch_name',
        'is_active', 'is_staff', 'is_superuser'
    )
    search_fields = (
        'username', 'ch_name',
    )
    list_filter = ('groups',)
