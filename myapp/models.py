from django.db import models


class people(models.Model):
    name = models.CharField(max_length=10)
    email = models.EmailField(max_length=20)
    phone = models.IntegerField()
    role = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)


class appointment(models.Model):
    patient = models.ForeignKey(people,on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    is_active = models.BooleanField(default=True)