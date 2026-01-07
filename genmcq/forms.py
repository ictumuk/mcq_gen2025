from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(UserCreationForm):
    """Custom registration form with styled fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'example@email.com',
            'autocomplete': 'email',
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tên đăng nhập',
            'autocomplete': 'username',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'new-password',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được sử dụng.')
        return email


class LoginForm(AuthenticationForm):
    """Custom login form with styled fields"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tên đăng nhập hoặc Email',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'autocomplete': 'current-password',
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500',
        })
    )


class ProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Họ'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tên'}),
        }


# =============================================================================
# Chat Room Forms (CR-BE-040, CR-BE-041, CR-BE-042)
# =============================================================================

class RoomCreateForm(forms.Form):
    """Form for creating a new chat room"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Tên phòng chat',
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Mô tả phòng (tùy chọn)',
            'rows': 2,
        })
    )
    room_type = forms.ChoiceField(
        choices=[
            ('community', 'Cộng đồng'),
            ('work', 'Công việc'),
            ('ai_deep', 'Chuyên sâu AI'),
        ],
        widget=forms.RadioSelect(attrs={'class': 'form-radio'})
    )
    has_password = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mật khẩu (nếu có)',
        })
    )
    bot_enabled = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class RoomJoinForm(forms.Form):
    """Form for joining a password-protected room"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Nhập mật khẩu phòng',
            'autofocus': True,
        })
    )


class RoomSettingsForm(forms.Form):
    """Form for room settings (host only)"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 3,
        })
    )
    room_type = forms.ChoiceField(
        choices=[
            ('community', 'Cộng đồng'),
            ('work', 'Công việc'),
            ('ai_deep', 'Chuyên sâu AI'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    has_password = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mật khẩu mới (để trống nếu không đổi)',
        })
    )
    bot_enabled = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )
