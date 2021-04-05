from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    # upload_to : 이미지를 저장할 폴더의 경로 규칙을 지정, blank=True를 하면 필수 항목이 아니게 된다
    # python -m pip install Pillow
    head_image = models.ImageField(upload_to = 'blog_app/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog_app/files/%Y/%m/%d/', blank=True)
    # 포스트 생성시 자동으로 저장되는 모델, auto_now_add=True 처음 레코드가 생성될 때 자동으로 저장
    created_at = models.DateTimeField(auto_now_add=True)
    # 수정 시 자동으로 저장되는 모델, auto_now=True 다시 저장할때 자동으로 저장
    update_at = models.DateTimeField(auto_now=True)
    # author : 추후 작성 예정

    # django admin Post 모델 제목
    def __str__(self):
        # {self.pk} : 해당 포스트의 pk 값
        # {self.title} 해당 포스트의 title 값
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'