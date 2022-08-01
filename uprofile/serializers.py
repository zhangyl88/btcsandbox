from rest_framework import serializers

from account.models import Account


# Update Profile Serializer
class UpdateProfileSerializer(serializers.ModelSerializer):
    username                = serializers.CharField()
    
    class Meta:
        model               = Account
        fields              = ['username', 'fullname']


class UpdateEmailSerializer(serializers.Serializer):
    email                   = serializers.EmailField()