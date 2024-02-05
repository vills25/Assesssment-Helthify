from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login_view'),
    path('signup_view/', signup_view, name='signup_view'),
    path('forget_password_view/', forget_password_view, name='forget_password_view'),
    path('otp_verification_view/', otp_verification_view, name='otp_verification_view'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('home_view/', home_view, name='home_view'),
    path('all_doctors_view/', all_doctors_view, name='all_doctors_view'),
    path('doctor_detail_view/<int:doctor_id>/', doctor_detail_view, name='doctor_detail_view'),
    path('book_appointment_view/<int:doctor_id>/', book_appointment_view, name='book_appointment_view'),
    path('my_appointments/', my_appointments, name='my_appointments'),
    path('delete_appointment/<int:appointment_id>/', delete_appointment, name='delete_appointment'),
    path('update_appointment_status/<int:appointment_id>/', update_appointment_status, name='update_appointment_status'),
    path('update_profile_view/', update_profile_view, name='update_profile_view'),
    path('logout/', logout, name='logout'),
    
]
