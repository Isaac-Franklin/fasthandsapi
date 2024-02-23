from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from userregapp.models import UserRegisterModel
from django.contrib.auth.models import User


class CheckUserData(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)        
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))
        
    def create_user(self, first_name, last_name, email, location, phone, skill, password, NIN, **kwargs):
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("An email address is required"))
        
        if not first_name:
            raise ValueError(_("A full name is required"))
        
        if not last_name:
            raise ValueError(_("A location is required"))
        
        user = User.object.create(email=email, first_name=first_name, last_name=last_name, **kwargs)
        user.set_password = password
        # user.save()
        UserRegisterModel.objects.create(email=email, fullname = first_name + " " + last_name, location=location, 
                                    PhoneNumber=phone, Skill = skill, Password = password, NIN=NIN)