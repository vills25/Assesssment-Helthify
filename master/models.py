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
        
class Role(BaseClass):
    doctor_ = 'Doctor'
    patient_ = 'Patient'
    
    choice_ = [(doctor_, 'Doctor'),
               (patient_, 'Patient'),
              ]            
    name = models.CharField(max_length=255, choice = choice_)
    
    def __str__(self): 
        return f'{self.name}'
    
class signed_up(BaseClass):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    title = models.CharField(max_length =255, blank =True)
    firstname = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    gender = models.CharField(max_length = 255,blank = True)
    degree = models.CharField(max_length=255, blank = True)
    email = models.EmailField(max_length = 255, unique=True)
    contact = models.CharField(max_length = 255)
    address = models.TextField(blank = True)
    summary = models.TextField(blank = True)
    otp = models.CharField(max_length=10, default="658734", blank=True)
    password = models.CharField(max_length = 255, blank = True)
    credentials_sent = models.BooleanField(default = False)
    is_activated_patient = models.BooleanField(default = True)
    is_activated_doctor = models.BooleanField(default = False)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname} - {self.role}"
    
    def save(self, *args, **kwargs):
        if not  self.password:
            self.password = generate_uniques.generate_password()
        
        if not self.credentials_sent:
            name = f'{self.firstname.upper()} {self.lastname.upper()}'
            subject = f"Login Credentials from Healthify for {name}"
            message = f"welcome to Healthify! Now you can Login with your Email: {self.email} and password: {self.password}"
            from_email = settings.EMAIL_HOST_USER
            rec_list = [f"{self.email}"]
            
            send_mail(subject,message,from_email,rec_list)

            self.credentials_sent = True

        super(signed_up, self).save(*args, **kwargs) 
                    
        
    