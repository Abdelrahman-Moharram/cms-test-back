from rest_framework.response import Response
from rest_framework import status

from accounts.Permissions import permission_allowed
from rest_framework.decorators import api_view
from project.helper import paginate_query_set_list
from .models import Role, Role_Permission, Module, Permission
from .serializer import RolesListSerializer, IncludedRoleSerial
from .forms import role_form

@api_view(['GET',])
@permission_allowed('permissions.roles.view')
def list_roles(request):
    roles               = Role.objects.order_by('name').all() #.values('name', 'id', 'created_at', 'created_by')
    data                = paginate_query_set_list(roles, request.GET, RolesListSerializer, 'roles')
    return Response(
        data, 
        status=status.HTTP_200_OK
    )
    
@api_view(['POST',])
@permission_allowed('permissions.roles.add')
def add_role(request):
    form            = role_form(data = request.POST)
    if form.is_valid():
        form.save(created_by=request.user)

        return Response({
                'message': f'تم إضافة الدور "{request.POST['name']}" بنجاح'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
            'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT',])
@permission_allowed('permissions.roles.edit')
def edit_role(request, id):
    role                = Role.objects.filter(id=id).first()
    old_name            = role.name
    if not role:
        return Response(
            {
                'error': "this role doesn't exist or may be deleted"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    form            = role_form(data=request.POST, instance=role)
    if form.is_valid():
        form.save(created_by=request.user)

        return Response({
                'message': f'تم تعديل الدور من "{old_name}" إلى "{request.POST['name']}" بنجاح'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
            'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET',])
@permission_allowed('permissions.roles.view')
def role_details(request, id):
    role                = Role.objects.filter(id=id).first()
    if not role:
        return Response(
            {
                'error': "this role doesn't exist or may be deleted"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    list_permissions    = dict()
    modules             = Module.objects.filter(is_editable=True)
    role_permission     = Role_Permission.objects.filter(role=role)

    for module in modules:    
        list_permissions[module.name] = []
        for permission in  module.permissions.values('id', 'key', 'label'):
            perm_dict = dict(permission)
            if role_permission.filter(permission__id=permission['id']).exists():
                perm_dict['has_perm'] = True
            else:
                perm_dict['has_perm'] = False

            list_permissions[module.name].append(perm_dict)
        

    


    return Response(
        {
            'role'              : IncludedRoleSerial(role).data,
            'permissions'       : list_permissions,
        }, 
        status=status.HTTP_200_OK
    )

@api_view(['PUT',])
@permission_allowed('permissions.roles.edit.permissions')
def add_permission_to_role(request, id):
    role                = Role.objects.filter(id=id).first()
    permission          = request.data.get('permission_id', None)
    
    if not role or not permission:
        return Response(
            {
                'error': "خطأ في الدور أو في الصلاحية"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    role_permission     = Role_Permission.objects.filter(role=role, permission__id=permission).first()

    if role_permission:
        role_permission.delete()
        return Response({
                    'message': f'تم حذف صلاحية {role_permission.permission.label} من {role.name}'
                },
                status=status.HTTP_201_CREATED
            )
    else:
        role_permission  = Role_Permission.objects.create(role=role, permission=Permission.objects.get(id=permission))
        role_permission.save()
        return Response({
                    'message': f'تم إضافة صلاحية {role_permission.permission.label} إلى {role.name}'
                },
                status=status.HTTP_201_CREATED
            )


@api_view(['GET',])
@permission_allowed('permissions.roles.edit')
def role_form_data(request, id):
    role                = Role.objects.filter(id=id).first()
    if not role:
        return Response(
            {
                'error': "this role doesn't exist or may be deleted"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
            
    return Response(
        {
            'role'              : IncludedRoleSerial(role).data,
        }, 
        status=status.HTTP_200_OK
    )

@api_view(['GET',])
@permission_allowed('permissions.roles.view')
def get_roles_as_selectlist(request):
    exclude = request.GET.get('exclude', None)
    if not exclude:
        return Response(
            {
                "roles":list(Role.objects.values('id', 'name')) 
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "roles":list(Role.objects.exclude(id=exclude).values('id', 'name')) 
        },
        status=status.HTTP_200_OK
    )

@api_view(['DELETE',])
@permission_allowed('permissions.roles.delete')
def delete_role(request, id):
    role        = Role.objects.filter(id=id).first()

    if 'alter_role' in request.data:
        alter_role  = request.data['alter_role']
    
    if not role:
        return Response(
            {
                'error': "هذا الدور غير موجود أو قد تم حذفه"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    if not alter_role:
        return Response(
            {
                'error': "يجب اختيار دور بديلة لإضافة المستخدمين اليها"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    alter_role  = Role.objects.filter(id=alter_role).first()
    if not role:
        return Response(
            {
                'error': "الدور البديل غير موجود أو قد تم حذفه"
            },
            status=status.HTTP_404_NOT_FOUND
        )
    if alter_role == role:
        return Response(
            {
                'error': "لا يجب ان يكون الدور البديل هو نفس الدور المحذوف"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if role.users:
        role.users.update(role=alter_role)
    role_name = role.name
    role.delete()
    return Response(
            {
                'message': f"تم حذف الدور {role_name} بنجاح"
            },
            status=status.HTTP_404_NOT_FOUND
        )


    


# To Do -> make delete function ask user to change the role of users already assigned to this role before deletion 