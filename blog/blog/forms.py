from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'thumb_image', 'file_upload', 'tags'] 

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

