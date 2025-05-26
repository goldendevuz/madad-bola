import random
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    student_phone = models.CharField(max_length=9, null=True, blank=True)
    parents_phone = models.CharField(max_length=9, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'

    def check_username(self):
        if not self.username:
            temp_username = f'user-{uuid.uuid4().__str__().split("-")[-1]}' # instagram-23324fsdf
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0,9)}"
            self.username = temp_username

    def check_email(self):
        if not self.email:
            temp_email = f'user-{uuid.uuid4().__str__().split("-")[-1]}' # instagram-23324fsdf
            while User.objects.filter(email=temp_email):
                temp_email = f"{temp_email}{random.randint(0,9)}"
            self.email = temp_email

    def check_pass(self):
        if not self.password:
            temp_password = f'password-{uuid.uuid4().__str__().split("-")[-1]}' #  123456mfdsjfkd
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()