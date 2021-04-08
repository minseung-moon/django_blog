from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# LoginRequiredMixin, 로그인 했을 때만 정상적으로 페이지가 보이도록 설정해주는 클래스
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category, Tag, Comment
# 권한에 따른 처리, 만약에 권한이 없는데 접근하면 403 오류 메시지 출력
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404

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
        context['comment_form'] = CommentForm
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
            # 태그와 관련된 작업을 하기 전에 createview의 form_validate()함수의 결과값을 response라는 변수에 임시 저장
            response = super(PostCreate, self).form_valid(form)

            # 장고가 자동으로 작성한 post_form.html의 폼을 보면 method="post"로 솔종ㄷ하오 있다
            # 아 폼 안에 name= 'tags_str'인 inputㄱ을 추가했으니 방문자가 <submit> 버튼을 클릭했을 때 이 값 역시 Post방식으로 postCrete까지 전달돤 상태
            # 이 값은 self.request.Post.get('tags_str')로 받을 수 있다
            # post 방식으로 전달된 정보 중 name='tags_str'인 input의 값을 가져오라는뜻
            tags_str = self.request.POST.get('tags_str')
            # 이 값이 빈 칸인 경우에는 태그와 관련된 어떤 동작도 할 필요가 없습니다
            # 따라서 if문으로 tag_str을 처리해야 할지 판단해야 합니다
            # tag_str이 존재한다면 여러 개의 태그가 들어오더라도 처리할 수있어야 하고, 세미콜론과 쉼표 모두 구분자로 처리되어야 합니다
            # tags_str로 받은 값의 쉼표를 세미콜론으로 모두 변경한 후 세미콜론으로 split해서 리스트 형태로 tags_list에 담는다
            if tags_str:
                tags_str = tags_str.strip()


                tags_str = tags_str.replace(',',';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    # tags_list에 리스트 형태로 담겨 있는 값은 문자열 형태이므로 tag 모델의 인스턴스로 변환하는 과정이 필요하다
                    # 일단 문자열 앞뒤로 공백이 있을 ㅜㅅ 있으므로 strip()으로으로 앞뒤의 공백을 제거
                    t = t.strip()
                    # 이 값을 name으로 갖는 태그가 있다면 가져오고, 없다면 새로 만듭니다
                    # get_or_create()는 두가지 값을 동시에 return 합니다
                    # 첫번째는 tag 모델의 인스턴스이고, 두번째는 이 인스턴스가 새로 생성되었는지를 나타내는ㄴ bool 형태의 값입니다
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    # 만약 같은 name을 갖는 태그가 없어 새로 생성했다면 아직 slug 값은 없는 상태이므로 slug 값을 생성해야 한다
                    # 관리자가 페이지에서 작업할 때는 자도으로 생성해줬지만 이번에는 get_or_create()메서드로 생성했기 때문에 발생하는 문제다
                    # 이런 경우에 대비하기 위해 장고는 slugfy()라는 함수를 제공한다
                    # 한글 태그가 입력되더라고 slugㄹ를 만들수 있도록 alliw_unicode=true로 설정
                    # 이 값을 태그ㅡ이 slug에 부여되고 저장하면 name과 slug필드를 모두 채운 상태로 저장된다
                    # slugfy()를 쓰려면 당연히 views.py파일의 상단에 import해줘야 한다
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    # 새로 태그를 만들었든, 기존에 존쟇ㅏ던 태그를 가져왔든 새로 만든 포스트의 tags필드에 추가해야 한다
                    #이때 self.object는 이번에 새로 만든 포스트를 의미
                    self.object.tags.add(tag)
            # 원하는 작업이 다 끝나면 새로 만든 포스트의 페이지로 이동해야 하므로 resoponse변수에 담아놓았던 CreateviewDml formvalida()의 결과값을 reutnr
            return response
        else :
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']
    template_name = 'blog/post_update_form.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)
        return context

    def form_valid(self,form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response

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

def new_comment(request, pk):
    # 로그인하지 않은 상태에서 댓글 폼이 포스트 상세 페이지에 보이지 않게 설정했지만 비정상적인 방법으로 new_comment로 접근하려는 시도가 있을 수 있다
    # 이런 경우에 대비해 로그인하지 않은 경우에는 PermittionDenied를 발생
    if request.user.is_authenticated:
        # new_comment() 함수는 pk를 인자로 받습니다
        # 이값으로 댓글을 달 포스트를 쿼리를 남려 가져온다
        # 물론 post = Post.object.get(pk=pk)를 불러올 수도있지만 해당하는 pk가 없는 경우에는 404오류를 발생시키도록 하기 위해 장고가 제공하는 get_object_or_404 기능 활용
        post = get_object_or_404(Post, pk=pk)

        # 폼을 작성한 후 <submit> 버튼을 클릭하면 POST 방식으로 전달
        # 그런데 어떤 사람이 브라우저에서 127..../new_comment/로 (get)입력하는 경우도 생각할 수 있겠죠
        # 이 경우는 POST가 아니라 GET방식으로 서버에 요청하게 되므러 그냥 pk=10인 포스트의 페이지로 리다이렉트 되도록 설정
        if request.method == 'POST':
            # 정상적으로 폼을 작성하고 POST 방식으로 서버에 요청이 들어왔다면 POST 방식으로 들러온 저보를 CommentForm의 형태로 가져온디
            comment_form = CommentForm(request.POST)
            # 이 폼이 유효하게 작성되었다면 해당 내용을 새로운 레코드를 만들어 데이터베이스에 저장
            # 이 때 comment_form.save(commit=False)로 바로 저장하는 기능을 잠시 미루고 comment_form에 담긴 정보로 Comment 인스턴트만 가져옵니다
            # ㅇ; 떼 cpmmentForm은 content 필드의 내용만 담고 있으므로 post 팔드는 pk로 가져온 포스트로 채우고, author필드는 로그인한 사용자의 정보로 채운다
            # 그 작없이끝나야 비로소 저장
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                # 마지막으러 comment의 URL로 리다이렉트를 한다
                # 해당 포스트의 상세 페이지에서 이 댓글이 작성되어 있는 위치로 브라우저가 이동
                return redirect(comment.get_absolute_url())
        else :
            return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        # 이번에는 get으로도 접근이 가능하므로 댓글 작성자와 현재 로그인한 유저를 비교한다
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else :
        raise PermissionDenied

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