from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers 
from .models import Profile
from rest_framework.validators import UniqueValidator 
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'nickname', 'email']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'nickname', 'email', 'password', 'profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile.nickname = profile_data.get('nickname', profile.nickname)
        profile.email = profile_data.get('email', profile.email)
        profile.save()

        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 일치하지 않습니다.")
        return value

    def save(self):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class RegisterSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())] # 중복 검사
    )
    nickname = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())] # 중복 검사
    )
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())] # 중복 검사
    )
    password = serializers.CharField(
        write_only = True, 
        required = True, 
        validators = [validate_password]
    ) # 비밀번호 유효성 검사(너무 짧은 비밀번호 등)
    password2 = serializers.CharField(
        write_only = True, 
        required = True
    ) # 비밀번호 확인 필드

    class Meta:
        model = get_user_model()
        fields = ['username', 'nickname', 'email', 'password']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        
        refresh = RefreshToken.for_user(user)  # 사용자의 토큰 생성

        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True) # write_only=True: password 필드는 읽기 전용으로 설정

    class Meta:
        model = User
        fields = ['username', 'password'] # 로그인 시 아이디와 비밀번호만 필요

    def validate(self, data):
        user = authenticate(**data)
        if user:
            refresh = RefreshToken.for_user(user)  # 사용자의 토큰 생성
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user
            }
        raise serializers.ValidationError("유효하지 않은 로그인입니다.")
    
class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')
        return value