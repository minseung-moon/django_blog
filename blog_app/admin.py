from django.contrib import admin
from .models import Post, Category

# Register your models here.
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    # Category 모댈의 name필드에 값이 입력됐을 때 자동으로 slug가 만들어진다
    prepopulated_fields = {'slug' : ('name', )}

admin.site.register(Category, CategoryAdmin)