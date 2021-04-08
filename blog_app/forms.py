from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields, Comment 필드 중 사용할 필드만 작성
        fields = ('content',)
        # 여러개의 필드 중 몇개만 빼서 사용할 경우, exclude 사용
        # exclude = ('post', 'author', 'create_at', 'modified_at',)