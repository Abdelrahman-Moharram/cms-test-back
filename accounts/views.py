from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import User, UserType
from .forms import user_form
from .Permissions import permission_allowed
from project.helper import paginate_query_set_list
from datetime import datetime, timezone
from roles.models import Role

from .serializers import(
    MyTokenObtainPairSerializer,
    UserSerial,
    ListUserSerial,
    DetailedUserSerial,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user_serial = UserSerial(data=[request.user], many=True)
    
    if not user_serial.is_valid():
        pass
    if len(user_serial.data)  < 1:
        return Response(
            data={'error':'no user data exists'},
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        data=user_serial.data[0],
        status=status.HTTP_200_OK
    )



class CustomTokenObtainPairView(TokenObtainPairView):
    serilizer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token    = response.data.get('access')
            refresh_token   = response.data.get('refresh')

            response.set_cookie(
                settings.AUTH_COOKIE,
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response

class CustomTokenRefreshView(TokenRefreshView):
    serilizer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    serilizer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)

@permission_classes([AllowAny])
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response




############################ - USER MODULE - #################################

@api_view(['GET',])
@permission_allowed('permissions.users.view')
def get_list(request):
    if 'filter' in request.GET:
        users       = User.objects.order_by('created_at').filter(Q(full_name__contains=request.GET.get('filter', None))|Q(username__contains=request.GET.get('filter', None)))
        
    else:
        users       = User.objects.order_by('created_at').select_related('role').all()
    
    
    data            = paginate_query_set_list(users, request.GET, ListUserSerial, 'users')


    return Response(
        data, 
        status=status.HTTP_200_OK
    )



@api_view(['GET',])
@permission_allowed('permissions.users.view')
def user_details(request, id):
    user = User.objects.select_related('role', 'user_type').filter(id=id).first()
    if not user:
        return Response(data={
                'message': 'هذا المستخدم غير موجود أو قد تم حذفه'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    
    user_serial     = DetailedUserSerial(user)
    return Response(
        {
            'user': user_serial.data,
        }, 
        status=status.HTTP_200_OK
    )


@api_view(['GET',])
@permission_allowed('permissions.users.add')
def get_add_user_dropdowns(request):
    roles       = list(Role.objects.order_by('name').values('id', 'name'))
    user_types  = list(UserType.objects.order_by('name').values('id', 'name'))

    # role_serial         = IncludedRoleSerial(roles, many=True)
    # user_role_serial    = IncludedUserTypeSerial(user_types, many=True)

    return Response(
        {
            'roles':roles,
            'user_types': user_types
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST',])
@permission_allowed('permissions.users.add')
def add_user(request):
    form = user_form(data=request.POST)
    if form.is_valid():
        form.save()

        return Response({
                'message': f'تم إضافة المستخدم "{request.POST['full_name']}" بنجاح'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
            'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST',])
@permission_allowed('permissions.users.add')
def seed_user(request):
    required_fields = ['username', 'full_name', 'role', 'user_type']
    data = request.POST
    errors = {}

    for field in required_fields:
        if field not in data:
            errors[field] = ['هذا الحقل مطلوب']
    
    if len(errors) > 0:
        return Response(errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    role     , _    = Role.objects.get_or_create(name=data['role'])
    user_type, _    = UserType.objects.get_or_create(name=data['user_type'])
    
    try:
        user = User.objects.create(
                    full_name=data['full_name'],
                    username=data['username'],
                    role=role,
                    user_type=user_type,
                    password=data['password'],
                )
        user.save()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['PUT',])
@permission_allowed('permissions.users.edit')
def edit_user(request, id):
    user = User.objects.filter(id=id).first()
    if not user:
        return Response(data={
                'message': 'هذا المستخدم غير موجود أو قد تم حذفه'
            },
            status=status.HTTP_404_NOT_FOUND
        )
    form = user_form(data=request.POST, instance=user)
    if form.is_valid():
        form            = form.save(created_by=request.user)
        form.updated_by = request.user
        form.updated_at = datetime.now(tz=timezone.utc)

        form.save()

        return Response({
                'message': f'تم تعديل المستخدم "{form.full_name}" بنجاح'
            },
            status=status.HTTP_201_CREATED
        )
    return Response({
        'errors': form.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(['GET',])
@permission_allowed('permissions.users.add')
def user_search(request):
    if 'query' not in request.GET:
        return Response({'error':'يجب إدخال بيانات البحث'})
    query   = request.GET['query']
    exclude = request.GET.get('exclude', None)

    users = User.objects.filter(
            Q(full_name__contains=query)|Q(username__contains=query)
        )
    if exclude:
        users = users.exclude(id=exclude)
    
    
    # users_serial = IncludedUserSerial(users.order_by('full_name'), many=True)

    users_list = list(users.order_by('full_name').values('id', 'username', 'full_name'))
    
    return Response(
        data={'users': users_list},
        status=status.HTTP_200_OK
    )

##############################################################################

############################ - Roles MODULE - ###############################



##############################################################################

############################ - LAYWER MODULE - ###############################

##############################################################################
