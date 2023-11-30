from django.db import models
from django.conf import settings

# 태그에 대한 모델을 정의합니다.
class Tag(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name

# 게시글에 대한 모델을 정의합니다.
class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    # 게시글의 내용입니다.
    content = models.TextField()
    thumb_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)
    # 게시글의 태그, Tag 모델을 참조합니다. 선택적 필드입니다.
    tags = models.ManyToManyField(Tag, blank=True)

    # 게시글의 제목을 반환하는 메서드입니다.
    def __str__(self):
        return self.title
    
    # 게시글의 절대 URL을 반환하는 메서드입니다.
    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    
# 댓글에 대한 모델을 정의합니다.
class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    user  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    # 댓글에 대한 대댓글
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True
        )
    # 댓글의 내용입니다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    content = models.TextField()
    
    
    def __str__(self):
        return f"Comment #{self.id}: {self.content[:50]}"
    
