from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class Teacher(models.Model):
    first_name = models.CharField(default='', max_length=250)
    last_name = models.CharField(default='', max_length=250)
    profile_picture = models.ImageField(upload_to="dp/", default='dp/None/no-img.png')
    email_address = models.EmailField(max_length=254, unique=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999-999-999-999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    room_number = models.CharField(default='', max_length=250)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Subject(models.Model):
    title = models.CharField(default='', max_length=250)

    def __str__(self):
        return self.title


class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
            Teacher, on_delete=models.CASCADE, related_name="subject_taught")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.teacher, self.subject)