from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    student_name = models.CharField(max_length=100)

    roll_no = models.CharField(max_length=20,unique=True)

    department = models.CharField(max_length=100)

    student_class = models.CharField(max_length=50)

    email = models.EmailField()

    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.student_name