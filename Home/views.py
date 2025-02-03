from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils import timezone
from django.urls import reverse
from .models import *
from category.models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags




def index(request):
    category=Category.objects.all()

    # if request.user.is_staff:
    #     return render(request, 'authentication/forbidden.html', status=403)
     
    return render(request,'index.html',{'category':category})

def register(request):
    if request.method == 'POST':   
      first_name=request.POST.get('first_name')
      last_name=request.POST.get('last_name')
      username=request.POST.get('username')
      email=request.POST.get('email')
      password=request.POST.get('password')

      user_error=False
      
      if User.objects.filter(username=username).exists():
          user_error=True
          messages.error(request,'Username already exists')
      if User.objects.filter(email=email).exists():
          user_error=True
          messages.error(request,'Email already exists')
      if len(password) < 7:
          user_error=True
          messages.error(request,'Password must be 6 length')
      if user_error:
          return redirect('register')
      else:
          newuser=User.objects.create_user(
              first_name=first_name,
              last_name=last_name,
             
              email=email,
              password=password,
              username=username
          )
          messages.success(request,'Account created successfuly')
          return redirect('login')          

    return render(request,'authentication/register.html')

def loginview(request):

    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid login credentials')
            return redirect('login')

    return render(request,'authentication/login.html')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')


        try:
            user = User.objects.get(email=email)

            
            otp_code = str(random.randint(1000, 9999))

            
            request.session['reset_email'] = email
            request.session['otp_code'] = otp_code
            request.session['otp_time'] = str(timezone.now())  

            
            email_html = render_to_string("emails/otp_email.html", {
                "user": user,
                "otp_code": otp_code,
                "site_url": f"{request.scheme}://{request.get_host()}/reset-password/",
                "current_year": timezone.now().year
            })
            email_text = strip_tags(email_html)  # Get plain text version for email clients that don’t support HTML

            # Send email
            email_message = EmailMultiAlternatives(
                subject="Password Reset OTP",
                body=email_text,  # Plain text version
                from_email=settings.EMAIL_HOST_USER,
                to=[email]
            )
            email_message.attach_alternative(email_html, "text/html")  # Attach HTML version
            email_message.send()

            return redirect('verify_otp')

        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('forgot_password')

    return render(request, 'authentication/forgot_password.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp_code')
        session_time = request.session.get('otp_time')

        if not session_otp or not session_time:
            messages.error(request, "OTP expired or invalid. Please request a new one.")
            return redirect('forgot_password')

        
        if entered_otp == session_otp:
            return redirect('reset_password') 
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
        
    if request.method == "GET" and request.GET.get('resend_otp'):
        email = request.session.get('reset_email')

        if email:
            otp_code = str(random.randint(1000, 9999))  # Generate a new OTP
            request.session['otp_code'] = otp_code  # Update session with new OTP
            request.session['otp_time'] = str(timezone.now())  # Update OTP generation time

            try:
                # Prepare the email content
                email_html = render_to_string("emails/otp_email.html", {
                    "otp_code": otp_code,
                    "site_url": f"{request.scheme}://{request.get_host()}/reset-password/",
                    "current_year": timezone.now().year
                })
                email_text = strip_tags(email_html)  # Get plain text version for email clients that don’t support HTML

                # Send the email
                email_message = EmailMultiAlternatives(
                    subject="Password Reset OTP",
                    body=email_text,  # Plain text version
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email]
                )
                email_message.attach_alternative(email_html, "text/html")  # Attach HTML version
                email_message.send()

                messages.success(request, "A new OTP has been sent to your email.")
            except Exception as e:
                messages.error(request, "There was an error sending the OTP. Please try again.")
        
        return redirect('verify_otp')
    return render(request, 'authentication/verify_otp.html')


def reset_password(request):
     
    email = request.session.get('reset_email')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('reset_password')

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            request.session.flush()

            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, "Something went wrong. Try again.")
            return redirect('forgot_password')
    return render(request, 'authentication/reset_password.html')


def logoutview(request):
    logout(request)
    return redirect('login')
