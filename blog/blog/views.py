from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.shortcuts import render

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(tags__name__icontains=q)).distinct()
        return qs

post_list = PostListView.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        post = form.save(commit=False)
        post.save()
        video = form.save(commit=True)
        video.user = self.request.user
        tag_names = form.cleaned_data['tags']
        if tag_names:  
            for tag_name in tag_names.split(','):
                tag, _ = Tag.objects.get_or_create(name=tag_name.strip())
                post.tags.add(tag)

        return super().form_valid(form)

post_new = PostCreateView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)

post_detail = PostDetailView.as_view()


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/form.html'

    def test_func(self): 
        return self.get_object().user == self.request.user

post_edit = PostUpdateView.as_view()


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        return get_object_or_404(Post, id=post.id)

post_delete = PostDeleteView.as_view()


# 댓글 생성 뷰
class CommentNewView(LoginRequiredMixin, CreateView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('blog:post_detail', pk)
        return render(request, 'blog/form.html', {'form': form})

    def get(self, request):
        form = CommentForm()
        return render(request, 'blog/form.html', {'form': form})

comment_new = CommentNewView.as_view()


# 댓글 수정 뷰
class CommentUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, post__pk=self.kwargs['post_pk'], pk=self.kwargs['comment_pk'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self): 
        return self.get_object().user == self.request.user

comment_edit = CommentUpdateView.as_view()


# 댓글 삭제 뷰
class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_confirm_delete.html'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Comment, post__pk=self.kwargs['post_pk'], pk=self.kwargs['comment_pk'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self): 
        return self.get_object().user == self.request.user

comment_delete = CommentDeleteView.as_view()


class CommentReplyView(LoginRequiredMixin, CreateView):
    def post(self, request, post_pk, comment_pk):
        post = get_object_or_404(Post, pk=post_pk)
        comment = get_object_or_404(Comment, pk=comment_pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.comment = comment
            reply.user = request.user
            reply.save()
            return redirect('blog:post_detail', post_pk)
        return render(request, 'blog/form.html', {'form': form})

    def get(self, request, post_pk, comment_pk):
        form = CommentForm()
        return render(request, 'blog/form.html', {'form': form, 'post_pk': post_pk, 'comment_pk': comment_pk})

comment_reply = CommentReplyView.as_view()


# 답글 수정 뷰
class ReplyUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self, comment__post__pk=self.kwargs['post_pk'], comment__pk=self.kwargs['comment_pk'], pk=self.kwargs['reply_pk'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self): 
        return self.get_object().user == self.request.user

reply_edit = ReplyUpdateView.as_view()


# 답글 삭제 뷰
class ReplyDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_confirm_delete.html'

    def get_object(self, queryset=None):
        return get_object_or_404(self, comment__post__pk=self.kwargs['post_pk'], comment__pk=self.kwargs['comment_pk'], pk=self.kwargs['reply_pk'])

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self): 
        return self.get_object().user == self.request.user

reply_delete = ReplyDeleteView.as_view()

