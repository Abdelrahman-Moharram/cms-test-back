from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, UserType





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "اسم المستخدم أو كلمة المرور غير صحيحة"
    }
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['id']             = str(user.id)
        token['username']       = str(user.username)
        token['full_name']      = str(user.full_name)
        token['role']           = str(user.role)
        # token['permissions']    = [i.permission.key for i in Role_Permission.objects.filter(role=user.role)]


        return token




class IncludedUserSerial(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id', 'username', 'full_name']

class IncludedUserTypeSerial(serializers.ModelSerializer):
    class Meta:
        model= UserType
        fields=['id', 'name']


class UserSerial(serializers.ModelSerializer):
    role        = serializers.ReadOnlyField(source='role.name')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role']



class ListUserSerial(serializers.ModelSerializer):
    # role        = serializers.ReadOnlyField(source='role.name')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role']
    
    def to_representation(self, instance):
    
        representation = dict()
        
        representation['id']                       = instance.id
        representation['الاسم بالكامل']            = instance.full_name
        representation['اسم المستخدم']             = instance.username
        representation['الدور']                    = instance.role.name if instance.role else ''


        return representation
    







class DetailedUserSerial(serializers.ModelSerializer):
    # role        = serializers.ReadOnlyField(source='role')
    # role        = serializers.ReadOnlyField(source='role')
    class Meta:
        model= User
        fields=['id', 'full_name', 'username', 'role', 'user_type']


class IncludedLawyerSerial(serializers.ModelSerializer):
    full_name   = serializers.SerializerMethodField()
    def get_full_name(self, obj):
        return obj.user.full_name
    class Meta:
        model= User
        fields=['id', 'full_name']

