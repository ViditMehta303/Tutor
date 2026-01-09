from django.conf import settings
from django.db import models

#class StudentProfile(models.Model):
 #   user = models.OneToOneField(
  #      settings.AUTH_USER_MODEL,
   #     on_delete=models.CASCADE,
    #    related_name="accounts_student_profile",  # <-- add this
    #)
    #grade = models.IntegerField(null=True, blank=True)


    #def __str__(self):
     #   return f"{self.user.username} (Grade: {self.grade_level})"
