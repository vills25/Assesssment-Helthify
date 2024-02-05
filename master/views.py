from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from master.utils import generate_uniques
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

def is_authenticated(view_function):
    def wrapper(request, *args, **kwargs):
        if 'email' in request.session:
            return view_function(request, *args, **kwargs)
        else:
            messages.info(request, "Please Login to access this feature")
            return redirect('login_view')
        
    return wrapper

def signup_view(request):
    new_signup = None 
    if request.method == 'POST':
        role_ = request.POST.get("role")
        firstname_ = request.POST.get("firstname").title()
        lastname_ = request.POST.get("lastname").title()
        email_ = request.POST.get("email")
        contact_ = request.POST.get("contact").title()

        if role_ and firstname_ and lastname_ and email_ and contact_:
            try:
                role_instance = Role.objects.get(name=role_)
                new_signup = signed_up.objects.create(
                    role=role_instance,
                    firstname=firstname_,
                    lastname=lastname_,
                    email=email_,
                    contact=contact_
                )    
                new_signup.save()
                messages.success(request,"Registration Successful!")
                return redirect("login_view")
            except:
                messages.error(request, "This Email is already exist. Please enter a diffrent email id.")
                return redirect("signup_view")  
            
    roles = Role.objects.all()
    return render(request, 'signup.html', {'roles': roles, 'new_signup': new_signup})

def login_view(request):
    if request.method == 'POST':
        email_ = request.POST['email']
        password_ = request.POST['password']
        
        try:
            get_active_accounts = signed_up.objects.get(email=email_)

            if get_active_accounts.role.name == "Doctor":
                try:
                    get_active_accounts = signed_up.objects.get(email=email_)

                except signed_up.DoesNotExist:
                    messages.info(request, 'Invalid staff_id or password')
                    return redirect('login_view')
                else:
                    print(get_active_accounts.is_activated_doctor)
                    if get_active_accounts.is_activated_doctor == True:
                        if password_ == get_active_accounts.password:
                            request.session['email'] = email_
                            request.session['title'] = get_active_accounts.title
                            request.session['id'] = get_active_accounts.id
                            request.session['role'] = get_active_accounts.role.name
                            request.session['firstname'] = get_active_accounts.firstname
                            request.session['lastname'] = get_active_accounts.lastname
                            request.session['gender'] = get_active_accounts.gender
                            request.session['degree'] = get_active_accounts.degree
                            request.session['contact'] = get_active_accounts.contact
                            request.session['address'] = get_active_accounts.address
                            request.session['summary'] = get_active_accounts.summary
                            request.session['is_activated_doctor'] = get_active_accounts.is_activated_doctor

                            if get_active_accounts.role.name == "Doctor":
                                messages.success(request, f"hello! {get_active_accounts.title} {get_active_accounts.firstname} {get_active_accounts.lastname}...logged in Successfull")
                                return redirect('home_view')
                            elif get_active_accounts.role.name == "Patient" :
                                messages.success(request, f"hello! {get_active_accounts.title} {get_active_accounts.firstname} {get_active_accounts.lastname}...logged in Successfull")
                                return redirect('home_view')
                        else:
                            messages.info(request, 'Invalid staff_id or password')
                            return redirect('login_view')
                    else:
                        messages.info(request, 'Your account is deactivated. Please contact to Admin for activate.')
                        return redirect('login_view')

            if get_active_accounts.role.name == "Patient":
                try:
                    get_active_accounts = signed_up.objects.get(email=email_)

                except signed_up.DoesNotExist:
                    messages.info(request, 'Invalid staff_id or password')
                    return redirect('login_view')
                else:
                    print(get_active_accounts.is_activated_patient)
                    if get_active_accounts.is_activated_patient == True:
                        if password_ == get_active_accounts.password:
                            request.session['email'] = email_
                            request.session['title'] = get_active_accounts.title
                            request.session['id'] = get_active_accounts.id
                            request.session['role'] = get_active_accounts.role.name
                            request.session['firstname'] = get_active_accounts.firstname
                            request.session['lastname'] = get_active_accounts.lastname
                            request.session['gender'] = get_active_accounts.gender
                            request.session['degree'] = get_active_accounts.degree
                            request.session['contact'] = get_active_accounts.contact
                            request.session['address'] = get_active_accounts.address
                            request.session['summary'] = get_active_accounts.summary
                            request.session['is_activated_patient'] = get_active_accounts.is_activated_patient

                            if get_active_accounts.role.name == "Doctor":
                                messages.success(request, f"hello! {get_active_accounts.title} {get_active_accounts.firstname} {get_active_accounts.lastname}...logged in Successfull")
                                return redirect('home_view')
                            elif get_active_accounts.role.name == "Patient" :
                                messages.success(request, f"hello! {get_active_accounts.title} {get_active_accounts.firstname} {get_active_accounts.lastname}...logged in Successfull")
                                return redirect('home_view')
                        else:
                            messages.info(request, 'Invalid staff_id or password')
                            return redirect('login_view')
                    else:
                        messages.info(request, 'Your account is deactivated. Please contact to Admin for activate.')
                        return redirect('login_view')

        except signed_up.DoesNotExist:
            messages.info(request, 'Invalid staff_id or password')
            return redirect('login_view')

    return render(request, 'login.html')

def forget_password_view(request):
    if request.method == 'POST':
        email_ = request.POST['email'].lower()
        try:
            check_user = signed_up.objects.get(email=email_)
        except signed_up.DoesNotExist:
            messages.info(request, "User doesn't exist")
            return redirect('login_view')
        else:
            if check_user:
                otp_ = generate_uniques.generate_otp()
                subject = "Authentication Code for Forgot password"
                message = f"Your OTP for Password Change is: {otp_}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [f"{email_}"]
                send_mail(subject, message, from_email, recipient_list)
                check_user.otp = otp_
                check_user.save()
                context = {'email': email_}
                return render(request, 'otp_verification.html', context)
    return render(request, 'forget_password.html')

def otp_verification_view(request):
    if request.method == 'POST':
        email_ = request.POST['email'].lower()
        otp_ = request.POST['otp']
        new_password_ = request.POST['new_password']
        confirm_password_ = request.POST['confirm_password']
        try:
            check_user = signed_up.objects.get(email=email_)
        except signed_up.DoesNotExist:
            messages.info(request, "User doesn't exist")
            return redirect('login_view')
        else:
            if check_user:
                if check_user.otp == otp_:
                    if new_password_ == confirm_password_:
                        check_user.password = new_password_
                        check_user.save()
                        messages.success(request, "Password Changed Successfully")
                        return redirect('login_view')
                    else:
                        messages.info(request, "New password and confirm password doesn't match!!")
                        context = {'email': email_}
                        return render(request, 'otp_verification.html', context)
                else:
                    messages.error(request, "Invalid OTP!!!")
                    context = {'email': email_}
                    return render(request, 'otp_verification.html', context)

    return render(request, 'otp_verification.html')

@csrf_protect
def resend_otp(request):
    if request.method == 'GET':
        email_ = request.GET.get('email')
        if email_:
            try:
                check_user = signed_up.objects.get(email=email_)
            except signed_up.DoesNotExist:
                print("User doesn't exist")
                return JsonResponse({'success': False, 'message': 'User does not exist'})

            if check_user:
                otp_ = generate_uniques.generate_otp()
                subject = "Authentication Code for Forgot password"
                message = f"Your OTP for Password Change: {otp_}"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [f"{email_}"]
                send_mail(subject, message, from_email, recipient_list)
                check_user.otp = otp_
                check_user.save()
                return JsonResponse({'success': True, 'email': email_})

    return JsonResponse({'success': False, 'message': 'Failed to resend OTP'})

@is_authenticated
def home_view(request):
    return render(request, "home.html")

@is_authenticated
def update_profile_view(request):
    if request.method == 'POST':
        title_ = request.POST['title']
        firstname_ = request.POST['firstname']
        lastname_ = request.POST['lastname']
        gender_ = request.POST['gender']
        contact_ = request.POST['contact']
        address_ = request.POST['address']
        summary_ = request.POST['summary']

        if request.session.get("role") == "Doctor":
            degree_ = request.POST['degree']

        request.session['title'] = title_
        request.session['firstname'] = firstname_.title()
        request.session['lastname'] = lastname_.title()
        request.session['gender'] = gender_.title()
        request.session['contact'] = contact_
        request.session['address'] = address_.title()
        request.session['summary'] = summary_.title()

        if request.session.get("role") == "Doctor":
            request.session['degree'] = degree_.upper()

        get_my_detail(request)
        messages.success(request, "Profile updated successfully.")
        return redirect('home_view')


    return render(request, 'update_profile.html')

@is_authenticated
def get_my_detail(request):
    user_id = request.session.get('id')
    my_profile = signed_up.objects.get(id=user_id)

    my_profile.title = request.session.get('title')
    my_profile.firstname = request.session.get('firstname')
    my_profile.lastname = request.session.get('lastname')
    my_profile.gender = request.session.get('gender')
    my_profile.contact = request.session.get('contact')
    my_profile.address = request.session.get('address')
    my_profile.summary = request.session.get('summary')

    if request.session.get("role") == "Doctor":
        my_profile.degree = request.session.get('degree')

    my_profile.save()

    return

@is_authenticated
def doctor_detail_view(request, doctor_id):
    try:
        doctor = signed_up.objects.get(id=doctor_id)
        return render(request, 'doctor_detail.html', {'doctor': doctor})
    except signed_up.DoesNotExist:
        messages.error(request, "Doctor not found.")
        return redirect('all_doctors_view')

@is_authenticated
def book_appointment_view(request, doctor_id):
    doctor = get_object_or_404(signed_up, id=doctor_id)

    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_email = request.POST.get('patient_email')
        patient_contact = request.POST.get('patient_contact')
        doctor_name = request.POST.get('doctor_name')
        doctor_email = request.POST.get('doctor_email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        additional_info = request.POST.get('additional_info')

        appointment = Appointment.objects.create(   
            patient=patient_name,
            patient_email=patient_email,
            patient_contact=patient_contact,
            doctor=doctor_name,
            doctor_email=doctor_email,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            additional_info=additional_info
        )
        messages.success(request, f"Appointment requested with Dr. {doctor.firstname} {doctor.lastname} on {appointment_date} at {appointment_time}")
        return redirect('my_appointments')

    return render(request, 'book_appointment.html', {'doctor': doctor})

@is_authenticated
def delete_appointment(appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()    
    return HttpResponseRedirect('/my_appointments/') 

@is_authenticated
def all_doctors_view(request):

    logged_in_doctor_id = request.session.get('id')
    doctors = signed_up.objects.filter(role__name="Doctor").exclude(id=logged_in_doctor_id).order_by('-id')

    return render(request, 'all_doctors.html', {'doctors': doctors})

@is_authenticated
def my_appointments(request):
    if request.session.get('role') == "Patient":
        user_email = request.session.get('email')
        appointments = Appointment.objects.filter(patient_email=user_email)
        return render(request, 'view_appointments.html', {'appointments': appointments})
    if request.session.get('role') == "Doctor":
        user_email = request.session.get('email')
        appointments = Appointment.objects.filter(doctor_email=user_email)
        return render(request, 'view_appointments.html', {'appointments': appointments})

@is_authenticated
def update_appointment_status(request, appointment_id):
    if request.method == 'POST':
        try:
            appointment = Appointment.objects.get(id=appointment_id)

            approval_status = request.POST.get('approval_status')
            if approval_status == 'approve':
                appointment.approval_status = True
            elif approval_status == 'pending':
                appointment.approval_status = False

            return_message = request.POST.get('return_message')
            appointment.return_message = return_message
            appointment.save()
            messages.success(request, "Appointment status and return message updated successfully.")
            return redirect('my_appointments')
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('home_view')
    else:
        return redirect('home_view')

def logout(request):
    request.session.clear()
    messages.success(request, "You are logged Out")
    return redirect('login_view')
