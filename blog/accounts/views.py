from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import DeleteView
from .forms import CustomUserCreationForm, PasswordChangeForm, UserDeleteForm  
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.views import View
from django.shortcuts import render, redirect

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # 해당 객체의 작성자와 요청 유저를 비교하여 권한 부여
        return obj.author == request.user

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('accounts:login')
    
signup = SignUpView.as_view()


class LoginView(LoginView):
    template_name = 'accounts/form.html'

login = LoginView.as_view()


class LogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('accounts:login')

logout = LogoutView.as_view()


class ProfileView(LoginRequiredMixin, TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = 'accounts/profile.html'

profile = ProfileView.as_view()

class PasswordChangeView(View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:logout')
        else:
            return render(request, 'accounts/change_password.html', {'form': form})
    
change_password = PasswordChangeView.as_view()
        
        
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    permission_classes = [IsAuthenticated]
    model = get_user_model()
    template_name = 'accounts/user_delete.html'  
    success_url = reverse_lazy('blog:post_list')  # 회원 탈퇴 후 리다이렉트할 URL

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        user = self.get_object()
        return user == self.request.user
    
user_delete = UserDeleteView.as_view()        
        
        
class UserDeleteRequestView(LoginRequiredMixin, TemplateView):
    permission_classes = [IsAuthenticated]
    template_name = 'accounts/user_delete.html'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_delete_form'] = UserDeleteForm  # 회원 탈퇴 시 비밀번호 확인을 위한 폼
        return context
    
user_delete_request = UserDeleteRequestView.as_view()   