import os
import json
import threading
from django.views import View
from django.contrib import auth
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from validate_email import validate_email
from django.core.mail import EmailMessage
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

# Create your views here.

class EmailThread(threading.Thread):

    # constructor method
    def __init__(self,email):
        self.email = email      # self.email is an instance attribute(each instance created will have its own email value)
        threading.Thread.__init__(self)
        # super().__init__()   This is equivalent to threading.Thread.__init__(self)


    def run(self):
        self.email.send(fail_silently=False)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use, choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use, choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        
        # GET USER DATA
        # VALIDATE
        # create a user account
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST         #  (in case there are validation errors, so the user’s input can be retained).
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context=context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
              
                email_contents = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),                 # force_bytes: Converts data to bytes, ensuring it’s in the correct format for encoding.# Output: <class 'bytes'>
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={'uidb64': email_contents['uid'], 
                                                   'token': email_contents['token']         # since, path('activate/<uidb64>/<token>',VerificationView.as_view(), name='activate'),
                                                   })
              
                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link
                email_body =  'Hi '+ user.username + ', Please use the link below to activate your account \n'+activate_url

                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email],
                )

                # Add an Attachment file
                attachment_path = os.path.join(settings.BASE_DIR,'IncomeExpense','static','img','register.jpg')
                email.attach_file(path=attachment_path)

                #Send email using Thread
                EmailThread(email).start()

                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))       #The base64 encoded uidb64 is decoded using urlsafe_base64_decode() and converted back to a string using force_str()
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                messages.info(request, 'Your account is already activated. <br>You can log in now.')
                return redirect('login'+'?message='+'User already activated')
            
            if user.is_active:
                messages.info(request, 'User already activated')
                return redirect('login')
            
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            messages.error(request, 'An error occurred during account activation. Please try again later.')
            return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username +' you are now logged in')
                    return redirect(reverse('expenses'))
                
                
                messages.error(request, 'Account is not active, please activate using your email')
                return render(request, 'authentication/login.html')
            
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill in all the fields')
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
    

class RequestPasswordResetEmail(View):
    def get(self,request):
        return render(request,'authentication/reset-password.html')
        
    def post(self, request):
        email = request.POST['email']

        context = {
            'values':request.POST
        }
       
        if not validate_email(email):
            messages.error(request,"Please Enter a Valid Email")
            return render(request,'authentication/reset-password.html',context=context)

        user = User.objects.filter(email = email)

        if user.exists():

            current_site = get_current_site(request)
                
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),                 # force_bytes: Converts data to bytes, ensuring it’s in the correct format for encoding.# Output: <class 'bytes'>
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('reset-user-password', 
                           kwargs={'uidb64': email_contents['uid'], 
                                   'token': email_contents['token']})

            email_subject = 'Reset your account Password'

            reset_url = 'http://'+current_site.domain+link
            email_body =  'Hi there,' + ' Please use the link below to reset your account password \n' + reset_url

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email],
            )

            #Send email using thread
            EmailThread(email).start()
        
        messages.success(request, "If the email exists in our system, a password reset link has been sent to your inbox.")
        return render(request,'authentication/reset-password.html',context=context)
        


class CompletePasswordReset(View):
    def get(self,request,uidb64,token):

        context = {
            'uidb64' : uidb64,
            'token' : token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk=user_id)  

            if not PasswordResetTokenGenerator().check_token(user=user,token=token):
                messages.info(request,'Password Link is invalid, please request a new one')
                return render(request,'authentication/reset-password.html')
            
            #Token is valid
            return render(request,'authentication/set-newpassword.html',context=context)
            
        except Exception as ex:
            messages.error(request, 'An error occurred. Please try again later.')
            return render(request, 'authentication/reset-password.html', context)
            
    

    def post(self,request,uidb64,token):
        context = {
            'uidb64' : uidb64,
            'token' : token
        }

        password = request.POST['password']
        new_password = request.POST['passconfirm']

        if password != new_password:
            messages.error(request,'Passwords do not match')
            return render(request,'authentication/set-newpassword.html',context)
        
        if len(password) < 6:
            messages.error(request,'Password too short')
            return render(request,'authentication/set-newpassword.html',context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64)) 
            user = User.objects.get(pk=user_id)      
            user.set_password(password)
            user.save()

            messages.success(request,'Password reset successfull, You can login with your new password')
            return redirect('login')
        
        except Exception as ex:
            messages.info(request,'Something went wrong !!!')
            return render(request,'authentication/set-newpassword.html')