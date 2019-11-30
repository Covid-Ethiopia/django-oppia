# oppia/profile/models.py

from django.contrib.auth.models import User
from django.db import models

from oppia.models import Participant


class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True, default=None)
    can_upload = models.BooleanField(default=False)
    job_title = models.TextField(blank=True, null=True, default=None)
    organisation = models.TextField(blank=True, null=True, default=None)
    phone_number = models.TextField(blank=True, null=True, default=None)

    def get_can_upload(self):
        if self.user.is_staff:
            return True
        return self.can_upload

    def get_can_upload_activitylog(self):
        if self.user.is_staff:
            return True
        return False

    def is_student_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user,
                                           role=Participant.TEACHER).count()
        if teach > 0:
            return False
        else:
            return True

    def is_teacher_only(self):
        if self.user.is_staff:
            return False
        teach = Participant.objects.filter(user=self.user,
                                           role=Participant.TEACHER).count()
        if teach > 0:
            return True
        else:
            return False


class CustomField (models.Model):

    DATA_TYPES = (
        ('str', 'String'),
        ('int', 'Integer'),
        ('bool', 'Boolean')
    )

    id = models.CharField(max_length=100, primary_key=True, editable=True)
    label = models.CharField(max_length=200, null=False, blank=False)
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    helper_text = models.TextField(blank=True, null=True, default=None)
    type = models.CharField(max_length=10,
                            choices=DATA_TYPES,
                            null=False,
                            blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.id


class UserProfileCustomField (models.Model):
    key_name = models.ForeignKey(CustomField, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value_str = models.TextField(blank=True, null=True, default=None)
    value_int = models.IntegerField(blank=True, null=True, default=None)
    value_bool = models.BooleanField(null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.key_name.id + ": " + self.user.username

    def __str__(self):
        return self.key_name.id + ": " + self.user.username

    def get_value(self):
        if self.value_bool is not None:
            return self.value_bool
        elif self.value_int is not None:
            return self.value_int
        else:
            return self.value_str
            
