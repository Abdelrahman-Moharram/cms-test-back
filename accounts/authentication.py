from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from ldap3 import Server, Connection, ALL, NTLM, SIMPLE

User = get_user_model()

LDAP_SERVER = "ldap://AD-PR-01.TAC.LOC"
BASE_DN = "dc=example,dc=com"
LDAP_USER_DN_TEMPLATE = "cn={},dc=example,dc=com"  # Adjust as needed

class LDAPBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None

        # Connect to LDAP server
        server = Server(LDAP_SERVER, get_info=ALL)
        user_dn = LDAP_USER_DN_TEMPLATE.format(username)

        try:
            conn = Connection(server, user=user_dn, password=password, authentication=SIMPLE, auto_bind=True)
            if conn.bind():
                # Check if user exists in Django database, if not, create one
                user, created = User.objects.get_or_create(username=username)
                return user
        except Exception as e:
            print(f"LDAP authentication failed: {e}")

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None



class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None