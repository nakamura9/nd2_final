from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    """class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        #self.fields["password"].widget.attrs
    """
    def save(self):
        user = super(SignUpForm, self).save()

        return user