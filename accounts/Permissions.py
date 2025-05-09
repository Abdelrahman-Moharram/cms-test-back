from roles.models import Role_Permission, Permission
from rest_framework import response, status 



def permission_allowed(name):
    
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            if request.user and request.user.role and Role_Permission.objects.filter(role=request.user.role, permission__key=name).exists():
                    return view_func(request,*args,**kwargs)
            else:
                return response.Response({'message':'ليس لديك صلاحية تنفيذ هذا الطلب'}, status=status.HTTP_403_FORBIDDEN) 
        return wrapper_func
    return decorator 
