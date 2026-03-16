from django.db import models
from accounts.models import StudentProfile


class Attendance(models.Model):

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)

    subject = models.CharField(max_length=100)

    date = models.DateField(auto_now_add=True)

    time = models.TimeField(auto_now_add=True)

    status = models.CharField(max_length=10, default='Present')


    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=['student', 'subject', 'date'],

                name='unique_attendance'

            )

        ]


    def __str__(self):

        return f"{self.student.user.username} - {self.subject} - {self.date}"