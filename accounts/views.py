from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, OTP
from .utils import generate_otp, send_email_otp, send_phone_otp
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('chat_home')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def send_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request,"User not found")
            return redirect('send_otp')
        
        otp = generate_otp()

        if email:
            OTP.objects.create(user=user, otp_code=otp, purpose='email')
            send_email_otp(email,otp)
            request.session['otp_user'] = user.id
            request.session['otp_purpose'] = 'email'

        elif phone:
            OTP.objects.create(user=user, otp_code=otp, purpose='phone')
            send_phone_otp(phone,otp)
            request.session['otp_user'] = user.id
            request.session['otp_purpose'] = 'phone'

        return redirect('verify_otp')
    
    return render(request,'accounts/send_otp.html')


def verify_otp_view(request):
    if request.method=='POST':
        code = request.POST.get('otp')
        user_id = request.session.get('otp_user')
        purpose = request.session.get('otp_purpose')

        otp_obj = OTP.objects.filter(
            user_id=user_id,
            purpose = purpose,
            otp_code = code,
            is_verified = False,
            created_at__gte = timezone.now() - timedelta(minutes=5)
            ).first()
        
        if otp_obj:
            otp_obj.is_verified = True
            otp_obj.save()

            user = otp_obj.user
            if purpose == 'email':
                user.is_email_verified = True
            else:
                user.is_phone_verified = True
            user.save()

            login(request,user)
            return redirect('chat_home')
        
        messages.error(request,'Invalid or expired OTP')

    return render(request, 'accounts/verify_otp.html')