from rest_framework import serializers
from .models import Role_Permission, Role, Permission
from project.helper import date_converter_or_None

class IncludedUserPermissionsSerial(serializers.ModelSerializer):
    permission = serializers.SerializerMethodField()

    def get_permission(self, obj):
        return obj.permission.key
        
    class Meta:
        model= Role_Permission
        fields=['permission']

class IncludedRoleSerial(serializers.ModelSerializer):
    class Meta:
        model= Role
        fields=['id', 'name']


class RolesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
    def to_representation(self, instance):
        repr = dict()

        repr['id']              = instance.id
        repr['الدور']           = instance.name
        repr['تاريخ الإضافة']   = date_converter_or_None(str(instance.created_at.strftime("%Y-%m-%d")), is_to_hijri=True)
        repr['أضيف بواسطة']    = str(instance.created_by)

        return repr

class IncludedPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = [
            'key',
            'label',
            'id'
        ]

# class RolePermissionsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Role
    
#     def to_representation(self, instance):
        



#         repr = dict()

#         repr['id']                  = instance.id
#         repr['name']                = instance.name
#         repr['created_at']          = instance.created_at.strftime("%Y-%m-%d %H:%M")
#         repr['created_by']          = str(instance.created_by)
        
#         return repr