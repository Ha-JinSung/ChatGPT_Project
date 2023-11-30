
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (
    RegisterSerializer,
    PasswordChangeSerializer,
    
)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        # Implement login logic here
        return Response({'message': 'Login logic here'})

    @action(detail=False)
    def logout(self, request):
        # Implement logout logic here
        return Response({'message': 'Logout logic here'})

    @action(detail=False)
    def profile(self, request):
        # Implement profile view logic here
        return Response({'message': 'Profile view logic here'})

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # Implement password change logic here
            return Response({'message': 'Password changed successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
