from django.db import models
from .utils import generate_uniques
from django.conf import settings
from django.core.mail import send_mail
import random
import string

class BaseClass(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Role(models.Model):
    DOCTOR = 'Doctor'
    PATIENT = 'Patient'

    name = models.CharField(max_length=255, choices=[
        (DOCTOR, 'Doctor'),
        (PATIENT, 'Patient'),
    ])

    def __str__(self):
        return self.name
    
class signed_up(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, blank=True)
    degree = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    summary = models.TextField(blank=True)
    otp = models.CharField(max_length=10, default="658734", blank=True)
    password = models.CharField(max_length=255, blank=True)
    credentials_sent = models.BooleanField(default=False)
    is_activated_patient = models.BooleanField(default=True)
    is_activated_doctor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.role}"

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = generate_uniques.generate_password()

        if not self.credentials_sent:
            send_mail(
                f"Login Credentials from Healthify for {self.firstname.upper()} {self.lastname.upper()}",
                f"Welcome to Healthify! Now you can login with your Email: {self.email} and Password: {self.password}",
                settings.EMAIL_HOST_USER,
                [self.email]
            )
            self.credentials_sent = True

        super().save(*args, **kwargs) 
                    
class Appointment(models.Model):
    appointment_number = models.CharField(max_length=255, blank=True)
    patient = models.CharField(max_length=255, blank=True)
    patient_email = models.EmailField(max_length=255, blank=True)
    patient_contact = models.CharField(max_length=255, blank=True)
    doctor = models.CharField(max_length=255, blank=True)
    doctor_email = models.EmailField(max_length=255, blank=True)
    appointment_date = models.DateField(blank=True)
    appointment_time = models.TimeField(blank=True)
    additional_info = models.TextField(blank=True)
    return_message = models.TextField(blank=True)
    approval_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.appointment_number} : {self.patient} - {self.doctor} - {self.approval_status}"

    def save(self, *args, **kwargs):
        if not self.appointment_number:
            self.appointment_number = f"APN00{''.join(random.choices(string.digits, k=10))}"
        super().save(*args, **kwargs)        
    