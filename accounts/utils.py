import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email_otp(email,otp):
    send_mail(
        subject="Your OTP code",
        message=f"Your OTP is {otp}",
        from_email = "no-reply@smartchat.com",
        recipient_list = [email],
        fail_silently=False,
    )

def send_phone_otp(phone,otp):
    print(f"[SIMULATED SMS] OTP for {phone}:{otp}")