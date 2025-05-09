from rest_framework import serializers
from .models import User
import re
from datetime import datetime, timezone

class user_form(serializers.ModelSerializer):
    password = serializers.CharField(required=False)
    class Meta:
        model  = User
        fields = [
            'username',
            'full_name',
            'role',
            'user_type',
            'password',
        ]
    @property
    def is_update(self):
        return self.instance is not None
    def validate_username(self, value):
        old_user = User.objects.filter(username=value)
        if not self.is_update and old_user and old_user.exclude(self.instance).exists():
            raise serializers.ValidationError(f"اسم المستخدم موجود مسبقا")
        
        if not re.fullmatch('^[a-zA-Z][a-zA-Z0-9_. -]{2,}$', value):
            raise serializers.ValidationError(f"اسم المستخدم يجب ان يبدأ بأحرف ويحتوي على 3 أحرف على الأقل ولا يحتوي على [+%$#/|\\!]")
        return value
    
    def validate_password(self, value):
        
        if self.is_update and User.objects.filter(id=id).exists():
            id          = self.instance.pk
            return User.objects.filter(id=id).first().password
        else:
            if len(value) < 8:
                raise serializers.ValidationError(f"يجب أن تحتوي كلمة المرور على 8 أحرف على الأقل")
            
        return value
    
    def save(self, **kwargs):
        if self.is_update:
            self.instance.last_update_at = datetime.now(tz=timezone.utc)
            self.instance.updated_by = kwargs['created_by']
        return super().save(**kwargs)

                 
