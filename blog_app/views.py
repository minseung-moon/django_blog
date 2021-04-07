from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# LoginRequiredMixin, 로그인 했을 때만 정상적으로 페이지가 보이도록 설정해주는 클래스
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag
# 권한에 따른 처리, 만약에 권한이 없는데 접근하면 403 오류 메시지 출력
from django.core.exceptions import PermissionDenied

# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'
    # view의 해당하는 html 위치
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class PostCreate(LoginRequiredMixin ,CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def form_valid(self, form):
        # self.request.user, 웹 사이트 방문자를 의미
        current_user = self.request.user
        
        # is_authenticated, 방문자가 로그인 했는지 확인
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else :
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        # self.get_object(), updateview의 메소드로 post.object.get(pk=pk)랑 동일한 역할
        # 갖고온 post의 인스턴스에 저장된 author과 방문자와 동일한지 확인
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

def category_page(request, slug):
        if slug == 'no_category' :
            category = '미분류'
            post_list = Post.objects.filter(category=None)
        else :
            category = Category.objects.get(slug=slug)
            post_list = Post.objects.filter(category=category)

        return render(
            request,
            'blog/post_list.html',
            {
                'post_list' : post_list,
                'categories' : Category.objects.all(),
                'no_category_post_count' : Post.objects.filter(category=None).count(),
                'category' : category,
            }
        )

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list' : post_list,
            'tag' : tag,
            'categories' : Category.objects.all(),
            'no_categoru_post_count' : Post.objects.filter(category=None).count(),
        }
    )

# FBV
# def index(request):
#     posts = Post.objects.all().order_by('-pk')

#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts' : posts,
#         },
#     )

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)

#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post' : post,
#         }
#     )    