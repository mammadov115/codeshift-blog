from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Custom version of UserCreationForm that uses the project's custom User model.
    """

    class Meta(UserCreationForm.Meta):
        model = User  
        fields = ("username", "email", "password1")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Username field styling
        self.fields["password1"].widget.attrs.update({
            "class": "form-control"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control"
        })
