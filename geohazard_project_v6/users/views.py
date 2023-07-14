from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile
from concerns.models import Post, GuestPost, CombinedPost
from django.db.models import Q


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"Account successfully created for '{username}'")
			return redirect('login')
	else:
		form = UserRegisterForm()

	context = {
		'form': form
	}	
	return render(request, 'users/register.html', context)


@login_required
def profile(request):
	posts = Post.objects.all()
	guest_posts = GuestPost.objects.all()
	user_posts = Post.objects.filter(author=request.user)

	combined_posts = []

	for post in posts:
		combined_posts.append(CombinedPost(post=post))

	for guest_post in guest_posts:
		combined_posts.append(CombinedPost(guest_post=guest_post))

	combined_posts.sort(key=lambda post: post.get_latest_date(), reverse=True)

	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f"Your profile has been successfully updated!")
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
        'p_form': p_form,
        'posts': posts,
        'user_posts': user_posts,
        'guest_posts': guest_posts,
        'combined_posts': combined_posts
    }
	return render(request, 'users/profile.html', context)