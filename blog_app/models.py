from django.db import models
# user model은 장고에서 기본적으로 제공하는 모델이다
from django.contrib.auth.models import User
import os

# Create your models here.
# pip install django_extensions, django shell+, 설치 후 settings.py에 설정
# pip install ipython, django shell+

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # 사람이 읽을 수 있는 텍스트로 고유 URL을 만들고 싶을 때 주로 사용
    # allow_unicode=True를 통해서 한글로도 만들 수 있게 지정, 없으면 한글 지원 안됨
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'

    # admin에 표시될 이름
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
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

    # on_delete=models.CASCADE : 이 포스트의 작성자가 데이터베이스에서 삭제되었을 때 이 포스트도 같이 삭제
    # on_delete=models.SET_NULL : 이 포스터의 작성자가 삭제되면 같이 삭제 되지 않고 뮤명 값으로 출력
    # setNull 할 시 필드 값도 null 허동이 되어야 한다, null = True
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # blank = True, 관리자 페이지에서 카테고리를 빈 칸으로 지정할  수 있게 해준다
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 서로 여러 요소와 동시에 연결될 수 있는 다대다 관계, ManyToManyField
    # ManyToManyField는 기본적으로 null = True를 제공
    tags = models.ManyToManyField(Tag, blank=True)

    # django admin Post 모델 제목
    def __str__(self):
        # {self.pk} : 해당 포스트의 pk 값
        # {self.title} 해당 포스트의 title 값
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]