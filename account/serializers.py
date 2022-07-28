from rest_framework import serializers

from account.models import Account, TwoFactorOTP


# Create Account Serializer
class CreateAccountSerializer(serializers.ModelSerializer):

    password2               = serializers.CharField(style={'input_type' : 'password'}, write_only=True)

    class Meta:
        model               = Account
        fields              = ['email', 'password', 'password2']
        
        extra_kwargs = {'password' : {'write_only' : True}}

    def save(self):
        account = Account(
            email           = self.validated_data['email'],
        )

        password            = self.validated_data['password']
        password2           = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password' : 'Password must match.'})

        else:
            account.set_password(str(password))
            account.username = account.username.lower()
            account.save()

            return account


# Activate Account Serializer
class ActivateAccountSerializer(serializers.Serializer):
    code                    = serializers.IntegerField()


# Resend Account Activation Serializer
class ResendAccountConfirmSerializer(serializers.Serializer):
    email                   = serializers.EmailField()


# Login Serializer
class LoginSerialzier(serializers.Serializer):
    username                = serializers.CharField()
    password                = serializers.CharField(style={'input_type' : 'password'}, write_only=True)
    


# Confirm 2-Factor Authorization Serializer
class ConfirmAuthorizationSerializer(serializers.ModelSerializer):
    class Meta:
        model               = TwoFactorOTP
        fields              = ['code']


#!Forgot Password
# Reset Password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    email                   = serializers.EmailField()


# Confirm Reset Password Code Serializer
class ConfirmPasswordResetCodeSerializer(serializers.Serializer):
    email                   = serializers.EmailField()
    code                    = serializers.IntegerField()


# Set Password Serializer
class SetPasswordSerializer(serializers.Serializer):
    code                    = serializers.IntegerField()
    email                   = serializers.EmailField()
    password                = serializers.CharField(style={'input_type' : 'password'}, write_only=True)



# Check Username Availability
class CheckUsernameAvSerializer(serializers.Serializer):
    username                = serializers.CharField()


# Check Email Availability
class CheckEmailAvSerializer(serializers.Serializer):
    email                   = serializers.EmailField()


#!Forgot email
# Get Email with username Seriallizer
class GetEmailUsernameSerializer(serializers.Serializer):
    username                = serializers.CharField()