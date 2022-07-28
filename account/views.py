from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import authenticate
from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from btcsandbox.utils import (
    set_username, set_email, 
    otp_gen, tfa_gen, generate_username, search_list, emails,
)

from account.serializers import *
from account.models import *


# Register a user
class CreateView(APIView):
    authentication_classes      = permission_classes = []
    
    def post(self, request, format=None):
        response_data = {}
        serializer = CreateAccountSerializer(data=request.data)

        # If all data checks out
        if serializer.is_valid():
            user = serializer.save()
            
            # Generates a random username on creation
            set_username(generate_username(user.pk), user)
            
            otp = AccountConfirmationOTP.objects.create(user = user, code = otp_gen(),)

            # Send account activation mail
            subject         = 'Confirm your account'
            body            = render_to_string('email/account/confirm.html', {'code' : otp.code, 'user' : user})
            content         = strip_tags(body)
            mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [user.email])

            mail.attach_alternative(body, 'text/html')
            
            token = Token.objects.get(user=user)
            
            try:
                mail.send()

                response_data['status'] = status.HTTP_201_CREATED
                response_data['token'] = token.key
                response_data['success'] = True
                response_data['result'] = 'Account created.'

                return Response(data=response_data, status=response_data['status'])
        
            except Exception as e:
                response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                response_data['token'] = token.key
                response_data['success'] = True
                response_data['result'] = 'Account created. Cannot be confirmed at the moment.'
                response_data['error_log'] = f'{e}'

                return Response(data=response_data, status=response_data['status'])


        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])

        

# Confirm Account
class ConfirmView(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]
    
    def post(self, request, format=None):
        obj = self.request.user
        response_data = {}
        serializer = ActivateAccountSerializer(data=request.data)

        if serializer.is_valid():
            try:
                code = AccountConfirmationOTP.objects.get(code=serializer.validated_data['code'], user=obj)

                # Expired Code instance
                if code.is_used:
                    response_data['status'] = status.HTTP_226_IM_USED
                    response_data['success'] = False
                    response_data['result'] = 'OTP is expired.'

                    return Response(data=response_data, status=response_data['status'])

                # Active Code instance
                else:
                    code.confirm()
                    request.user.confirm()

                    response_data['status'] = status.HTTP_200_OK
                    response_data['success'] = True
                    response_data['result'] = 'Account confirmed.'

                    # Send account confirmed mail
                    subject         = 'Account Confirmed'
                    body            = render_to_string('email/account/confirmed.html', {'user' : obj})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [obj.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        return Response(data=response_data, status=response_data['status'])
                    
                    # When mail service is down
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['success'] = True
                        response_data['result'] = 'Account Confirmed. Cannot send emails at the moment.'
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

            # Invalid Code Instance
            except AccountConfirmationOTP.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'OTP is invalid.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


# Resend account confirmation OTP 
class ResendConfirm(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]

    def put(self, request, format=None):
        obj = self.request.user
        response_data = {}
        serializer = ResendAccountConfirmSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                code = AccountConfirmationOTP.objects.get(user=obj, is_used=False)

                # Send account activation mail
                subject         = 'Confirm your account'
                body            = render_to_string('email/account/confirm.html', {'code' : code, 'user' : obj})
                content         = strip_tags(body)
                mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [obj.email])

                mail.attach_alternative(body, 'text/html')

                # Resend without changing email
                if email == obj.email:
                    # Resend Activations
                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Confirmation Resent.'

                        return Response(data=response_data, status=response_data['status'])

                    # On Mail Service Failure
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['success'] = False
                        response_data['result'] = 'An error occurred. Cannot send activation code at the moment.'
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

                # Resend - Changing email
                else:
                    # Check if email is avaliable
                    if search_list(email, emails):
                        response_data['status'] = status.HTTP_400_BAD_REQUEST
                        response_data['success'] = False
                        response_data['result'] = 'Email is already in used.'
                        
                        return Response(data=response_data, status=response_data['status'])
                        
                    else:

                        try:
                            # Resend Activations
                            mail.send()
                            
                            # Update Email
                            set_email(email, obj)

                            response_data['status'] = status.HTTP_200_OK
                            response_data['success'] = True
                            response_data['result'] = 'Confirmation Resent to updated email.'

                            return Response(data=response_data, status=response_data['status'])

                        # On Mail Service Failure
                        except Exception as e:
                            response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                            response_data['success'] = False
                            response_data['result'] = 'An error occurred. Cannot send activation code at the moment.'
                            response_data['error_log'] = f'{e}'

                            return Response(data=response_data, status=response_data['status'])

            except AccountConfirmationOTP.DoesNotExist:
                response_data['status'] = status.HTTP_226_IM_USED
                response_data['success'] = False
                response_data['result'] = 'Account already activated.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


# Login account
class Authorize(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = LoginSerialzier(data=request.data)

        if serializer.is_valid():
            # Tries to authenticate user with given credentials
            account = authenticate(username=serializer.validated_data.get('username'), password=serializer.validated_data.get('password'))

            if account:
                preference = Preference.objects.get(user=account)

                try:

                    token = Token.objects.get(user=account)

                    # Returns the token as a response
                    response_data['status'] = status.HTTP_200_OK
                    response_data['token'] = f'{token.key}'
                    response_data['success'] = True
                    response_data['twoFactorEnabled'] = preference.two_factor_enabled
                    response_data['result'] = f'Logged in as {account.username}.'

                    # Updates the time of last login and saves the account
                    account.last_login = timezone.now()
                    account.save()

                    return Response(data=response_data, status=response_data['status'])

                except Token.DoesNotExist:
                    token = Token.objects.create(user=account)

                    # Returns the token as a response
                    response_data['status'] = status.HTTP_200_OK
                    response_data['token'] = f'{token.key}'
                    response_data['success'] = True
                    response_data['twoFactorEnabled'] = preference.two_factor_enabled
                    response_data['result'] = f'Logged in as {account.username}.'

                    # Updates the time of last login and saves the account
                    account.last_login = timezone.now()
                    account.save()

                    return Response(data=response_data, status=response_data['status'])

            # Invalid credentials instance
            else:
                response_data['status'] = status.HTTP_403_FORBIDDEN
                response_data['success'] = False
                response_data['result'] = 'Invalid credentials.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])
        

# Two Factor Generator
class TwoFactorGenerator(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]

    def get(self, request, format=None):
        obj = self.request.user
        response_data =  {}
        
        try:
            preference = Preference.objects.get(user=obj)

            # If 2-Factor is Ennabled
            if preference.two_factor_enabled:
                try:
                    code = TwoFactorOTP.objects.get(user=obj, is_used=False)

                    # Send to email
                    subject = 'Authorize Login'
                    body = render_to_string('email/account/confirm.html', {
                        'code' : code,
                        'user' : obj
                    })
                    content = strip_tags(body)
                    mail = EmailMultiAlternatives(
                        subject,
                        content,
                        settings.DEFAULT_ACCOUNT_FROM_EMAIL,
                        [obj.email]
                    )
                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Authorization sent.'

                        return Response(data=response_data, status=response_data['status'])
                
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot authorize login at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

                # Creates a new 2-factor OTP if it does not esxit
                except TwoFactorOTP.DoesNotExist:
                    code = TwoFactorOTP.objects.create(user=request.user, is_used=False, code=tfa_gen())
                    
                    # Send to email
                    subject = 'Authorize Login'
                    body = render_to_string('email/account/authorize.html', {
                        'code' : code,
                        'user' : obj
                    })
                    content = strip_tags(body)
                    mail = EmailMultiAlternatives(
                        subject,
                        content,
                        settings.DEFAULT_ACCOUNT_FROM_EMAIL,
                        [obj.email]
                    )
                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Authorization sent.'

                        return Response(data=response_data, status=response_data['status'])
                
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot authorize login at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

            # If 2-Factor is not enabled
            else:
                response_data['status'] = status.HTTP_401_UNAUTHORIZED
                response_data['result'] = '2-Factor is not enabled.'
                response_data['success'] = False

                return Response(data=response_data, status=response_data['status'])

        # If User Prference Does not Exist
        # Creates a new instance and reloops
        except Preference.DoesNotExist:
            preference = Preference.objects.create(user=obj)

            # If 2-Factor is Ennabled
            if preference.two_factor_enabled:
                try:
                    code = TwoFactorOTP.objects.get(user=obj, is_used=False)

                    # Send to email
                    subject         = 'Authorize Login'
                    body            = render_to_string('email/account/authorize.html', {'user' : obj, 'code': code})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [obj.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Authorization sent.'

                        return Response(data=response_data, status=response_data['status'])
                
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot authorize login at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

                # Creates a new 2-factor OTP if it does not esxit
                except TwoFactorOTP.DoesNotExist:
                    code = TwoFactorOTP.objects.create(user=request.user, is_used=False, code=tfa_gen())
                    
                    # Send to email
                    subject         = 'Authorize Login'
                    body            = render_to_string('email/account/authorized.html', {'user' : obj, 'code': code})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [obj.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        # mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Authorization sent.'

                        return Response(data=response_data, status=response_data['status'])
                
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot authorize login at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

            # If 2-Factor is not enabled
            else:
                response_data['status'] = status.HTTP_401_UNAUTHORIZED
                response_data['result'] = '2-Factor is not enabled.'
                response_data['success'] = False

                return Response(data=response_data, status=response_data['status'])
            
    
# Confirm Authorization
class ConfirmAuthorization(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]

    def put(self, request, format=None):
        obj = self.request.user
        response_data = {}
        serializer = ConfirmAuthorizationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Valid code instance
                code = TwoFactorOTP.objects.get(user=obj, code=serializer.validated_data.get('code'), is_used=False)

                code.is_used = True
                code.save()

                response_data['status'] = status.HTTP_202_ACCEPTED
                response_data['success'] = True
                response_data['result'] = 'Authorized.'

                return Response(data=response_data, status=response_data['status'])

            # Invalid Code Instance
            except TwoFactorOTP.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'OTP is invalid.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])
        

#!Forgot Password
# Reset Password
class ResetPassword(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data =  {}
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = Account.objects.get(email=serializer.validated_data.get('email'))

                try:
                    code = PasswordOTP.objects.get(user=user, is_used=False)

                    subject         = 'Reset Password'
                    body            = render_to_string('email/account/password/reset.html', {'code' : code, 'user' : user})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [user.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Password reset code sent.'

                        return Response(data=response_data, status=response_data['status'])

                    # Mail service failure
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot reset password at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

                except PasswordOTP.DoesNotExist:
                    code = PasswordOTP.objects.create(user=user, is_used=False, code=otp_gen())

                    subject         = 'Reset Password'
                    body            = render_to_string('email/account/password/reset.html', {'code' : code, 'user' : user})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives(subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [user.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Password reset code sent.'

                        return Response(data=response_data, status=response_data['status'])

                    # Mail service failure
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot reset password at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'Account not found.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


# Confirm Password Reset Code
class ConfirmPasswordResetCode(APIView):
    authentication_classes      = permission_classes = []

    def put(self, request, format=None):
        response_data = {}
        serializer = ConfirmPasswordResetCodeSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Recheck email
                user = Account.objects.get(email=serializer.validated_data.get('email'))

                try:
                    # Filter DB for given OTP
                    code = PasswordOTP.objects.get(user=user, is_used=False, code=serializer.validated_data.get('code'))

                    response_data['status'] = status.HTTP_302_FOUND
                    response_data['success'] = True
                    response_data['result'] = 'Password OTP is valid.'

                    return Response(data=response_data, status=response_data['status'])

                # Password otp invalid instance
                except PasswordOTP.DoesNotExist:
                    response_data['status'] = status.HTTP_406_NOT_ACCEPTABLE
                    response_data['success'] = False
                    response_data['result'] = 'Password OTP is invalid.'

                    return Response(data=response_data, status=response_data['status'])

            # Account not found instance
            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'Account not found.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


# Set password [Reset]
class SetPassword(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = SetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = Account.objects.get(email=serializer.validated_data.get('email'))

                try:
                    code = PasswordOTP.objects.get(code=serializer.validated_data.get('code'), user=user, is_used=False)

                    code.is_used = True
                    user.set_password(serializer.validated_data.get('password'))

                    code.save()
                    user.save()

                    subject         = 'Password Reseted'
                    body            = render_to_string('email/account/password/reseted.html', {'code' : code, 'user' : user})
                    content         = strip_tags(body)
                    mail            = EmailMultiAlternatives( subject, content, settings.DEFAULT_ACCOUNT_FROM_EMAIL, [user.email])

                    mail.attach_alternative(body, 'text/html')

                    try:
                        mail.send()

                        response_data['status'] = status.HTTP_200_OK
                        response_data['success'] = True
                        response_data['result'] = 'Password reseted.'

                        return Response(data=response_data, status=response_data['status'])

                    # Mail service failure
                    except Exception as e:
                        response_data['status'] = status.HTTP_417_EXPECTATION_FAILED
                        response_data['result'] = 'An error occurred. Cannot reset password at the moment.'
                        response_data['success'] = False
                        response_data['error_log'] = f'{e}'

                        return Response(data=response_data, status=response_data['status'])

                except PasswordOTP.DoesNotExist:
                    response_data['status'] = status.HTTP_406_NOT_ACCEPTABLE
                    response_data['success'] = False
                    response_data['result'] = 'Password OTP is invalid.'

                    return Response(data=response_data, status=response_data['status'])

            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'Account not found.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])
        

# Check Email Availabilty
class CheckEmailAv(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = CheckEmailAvSerializer(data=self.request.data)

        if serializer.is_valid():
            try:
                user = Account.objects.get(email=serializer.validated_data.get('email'))
                response_data['status'] = status.HTTP_226_IM_USED
                response_data['success'] = False
                response_data['result'] = 'Not Available.'

                return Response(data=response_data, status=response_data['status'])

            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = True
                response_data['result'] = 'Available.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])
        

# Check Username Availabilty
class CheckUsernameAv(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = CheckUsernameAvSerializer(data=self.request.data)

        if serializer.is_valid():
            try:
                user = Account.objects.get(username=serializer.validated_data.get('username'))
                response_data['status'] = status.HTTP_226_IM_USED
                response_data['success'] = False
                response_data['result'] = 'Not Available.'

                return Response(data=response_data, status=response_data['status'])

            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = True
                response_data['result'] = 'Available.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


#!Forgot Email
# Get email with username
class GetEmailUsername(APIView):
    authentication_classes      = permission_classes = []

    def post(self, request, format=None):
        response_data = {}
        serializer = GetEmailUsernameSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = Account.objects.get(username=serializer.validated_data.get('username'))

                response_data['status'] = status.HTTP_302_FOUND
                response_data['success'] = True
                response_data['result'] = user.email

                return Response(data=response_data, status=response_data['status'])

            except Account.DoesNotExist:
                response_data['status'] = status.HTTP_404_NOT_FOUND
                response_data['success'] = False
                response_data['result'] = 'Account not found.'

                return Response(data=response_data, status=response_data['status'])

        else:
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            response_data['success'] = False
            response_data['result'] = serializer.errors

            return Response(data=response_data, status=response_data['status'])


#! Logout  
# Logout all accounts
class LogoutAllAccounts(APIView):
    authentication_classes, permission_classes      = [TokenAuthentication], [IsAuthenticated]

    def put(self, request, format=None):
        response_data = {}
        obj = request.user

        try:
            old_token = Token.objects.get(user=obj)
            
            old_token.delete()

            # Creates a new token
            new_token = Token.objects.create(user=obj)

            response_data['status'] = status.HTTP_302_FOUND
            response_data['success'] = True
            response_data['token'] = new_token.key
            response_data['result'] = 'Logged out.'

            return Response(data=response_data, status=response_data['status'])

        except Token.DoesNotExist:
            # Creates a new token
            new_token = Token.objects.create(user=obj)

            response_data['status'] = status.HTTP_302_FOUND
            response_data['success'] = True
            response_data['token'] = new_token.key
            response_data['result'] = 'Logged out.'

            return Response(data=response_data, status=response_data['status'])