from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse_lazy
from django.utils import timezone
from posts.models import Post, Like
from .forms import UserProfileForm
from .models import UserProfile

@method_decorator(login_required(login_url=reverse_lazy('account_login')), name='dispatch')
class ProfileView(View):
    """Creating users profile pages 
    If method is GET it returns form of user profile
    If method is POST it saves data to database 
    """
    
    template_name = 'profile/profile.html'

    def get(self, request):

        profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(instance=profile)

        return render(request, self.template_name, {'form': form})

    def post(self, request):

        profile = get_object_or_404(UserProfile, user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if form.is_valid():
            form.cleaned_data['bio'] = request.POST.get('bio', '')
            form.cleaned_data['username'] = request.POST.get('username', '')
            form.cleaned_data['avatar'] = request.FILES.get('avatar', None)
            form.save()
            
            return redirect('profile')
        
        return render(request, self.template_name, {'form': form})
    
class ProfileDetailView(View):
    """Return user profile by pk"""

    template_name = 'profile/profile_for_others_users.html'

    def get(self, request, pk):

        user_profile = get_object_or_404(UserProfile, pk=pk)
        user_posts = Post.objects.filter(author=user_profile.user)
        users_likes = 0
        for post in user_posts:
            users_likes+=Like.objects.filter(post=post).count()
        
        user_rating = (user_posts.count() + users_likes*0.3) / (user_profile.user.date_joined - timezone.now()).days 

        return render(request, self.template_name, {'user': user_profile, 'user_posts': user_posts, 'rating':abs(round(user_rating, 2))})
