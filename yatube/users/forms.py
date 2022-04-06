from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm,
                                       PasswordResetForm)
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ChangeForm(PasswordChangeForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class PasswordReset(PasswordResetForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)
