from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from allauth.account.models import EmailAddress
from .forms import PostForm, CommentForm
from .models import Post, Comment, Like
from django.contrib import messages
from django.views import View 
import os

class PostsListView(View):
    """Return list of posts"""
    template_name = 'posts/index.html'
    posts_per_page = os.getenv('POST_PAGINATION')

    def get(self, request):
        
        post_list = Post.objects.select_related('author').only('title', 'author__username').order_by('-title')  #sort only important data for this page
        paginator = Paginator(post_list, self.posts_per_page)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)  

        return render(request, self.template_name, {'posts':posts})


class PostDetailView(View):
    """Return detail of posts or 404
    Also, it returns a form for live comments if the user has verified its email  
    If the method is GET, it returns the form, post, and all comments.
    If the method is POST, it saves a comment.
    """

    template_name = 'posts/post_detail.html'

    def CheckEmail(request):
        """Check is user auntificate his email
        """

        email_verified = False
        if request.user.is_authenticated:
            email_verified = EmailAddress.objects.filter(user=request.user,
                                                        verified=True).exists()
        return email_verified
    
    def get(self, request, pk):

        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(post=post)
        form = CommentForm()

        email_verified = PostDetailView.CheckEmail(request)

        context = {
            'post': post,
            'comments': comments,
            'form': form,
            'email_verified': email_verified,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):

        user = request.user
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm(request.POST)
        email_verified = PostDetailView.CheckEmail()
        
        if form.is_valid() and email_verified:
            comment = form.save(commit=False)
            comment.author = user
            comment.post = post
            comment.save()
            messages.success(request, 'Comment successfully added!')
        else:
            messages.error(request, 'Please correct the errors in the form.')

        context = {
        'post': post,
        'comments': Comment.objects.filter(post=post),
        'form': form,
        'email_verified': email_verified,
        }
        return render(request, self.template_name, context)

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

        form = self.form_class(request.POST, request.FILES)

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

        context = {
            'posts':result_posts,
            'query':query
        }
        return render(request, self.template_name, context)

class PostLike(View):
    
    def post(self, request, pk):
        
        try:
            post = get_object_or_404(Post, id=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if not created:
                like.delete()

            return redirect('post-home')
        except TypeError:   #user doesn't log in
            messages.error(request, "You're not login")
            return redirect('post-home')
        
class PostEditView(View):
    """Check is form valid and redirect to post.
    *Only author of the post can edit it
    """
    template_name = 'posts/post_edit.html'

    def get(self, request, pk, *args, **kwargs):

        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post-detail', pk=pk)
        return redirect('post-detail', pk=pk)
    
class PostDeleteView(View):

    def get(self, request, pk, *args, **kwargs):

        get_object_or_404(Post, pk=pk).delete()

        return redirect('post-home')