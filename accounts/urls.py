from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
    path('me/', me),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),

    #############################################################
    
    

    ###############################################################
    path("list/", get_list, name="get_list"),
    path("search/", user_search, name="user_search"),
    path("add/", add_user, name="add_user"),
    path("seed/", seed_user, name="seed_user"),
    path("<str:id>/", user_details, name="user_details"),
    path("<str:id>/edit/", edit_user, name="edit_user"),
    path("add/dropdowns/", get_add_user_dropdowns, name="get_add_user_dropdowns"),

    ###############################################################
    
]