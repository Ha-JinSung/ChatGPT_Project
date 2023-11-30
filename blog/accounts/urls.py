from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete/', views.user_delete, name='user_delete'),
    path('delete_request/', views.user_delete_request, name='user_delete_request'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views
# from rest_framework_simplejwt.views import TokenObtainPairView

# router = DefaultRouter()
# router.register('profile', views.profile, basename='profile')

# urlpatterns = [
#     router.urls,
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# ]