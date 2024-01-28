from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View 
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from allauth.account.models import EmailAddress

class PostsListView(View):
    """Return list of posts"""
    template_name = 'posts/index.html'
    posts_per_page = 3

    def get(self, request):
        post_list = Post.objects.select_related('author').only('title', 'author__username').order_by('-title')

        paginator = Paginator(post_list, self.posts_per_page)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  

        return render(request, self.template_name, {'posts':posts})


# views.py

class PostDetailView(View):
    """Return detail of posts or 404"""

    template_name = 'posts/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()

        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment successfully added!')
        else:
            messages.error(request, 'Please correct the errors in the form.')

        return redirect('post-detail', pk=pk)

class CreatePostView(View):
    """Create post class

    If the method is GET, it returns the post form. 
    If method is POST, it checks valid of data and add them to database 
    """
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def get(self, request):

        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-home') 
        
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    
class PostSearch(View):
    template_name = 'posts/search_results.html'

    def get(self, request):
        
        query = request.GET.get('q','')
        result_posts = Post.objects.filter(title__icontains=query)
        return render(request, self.template_name, {'posts':result_posts, \
                                                    'query':query})
    