from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post, GuestPost, CombinedPost
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.views import View


@method_decorator(login_required, name='dispatch')
class ReactView(View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        reacted_to_flag = False
        reacted_to_upvote = False

        # Check if the user has reacted to flag_react
        if post.flag_react.filter(id=user.id).exists():
            post.flag_react.remove(user)
            reacted_to_flag = True

        # Check if the user has reacted to upvote_react
        if post.upvote_react.filter(id=user.id).exists():
            post.upvote_react.remove(user)
            reacted_to_upvote = True

        # If the user hasn't reacted to flag_react 
        # and clicked the flag icon, add their reaction to flag_react
        if not reacted_to_flag and not reacted_to_upvote:
            post.flag_react.add(user)

        # If the user has already reacted to flag_react 
        # and clicked the upvote icon, add their reaction to upvote_react
        elif reacted_to_flag and not reacted_to_upvote:
            post.upvote_react.add(user)

        # If the user has already reacted to upvote_react 
        # and clicked the flag icon, add their reaction to flag_react
        elif not reacted_to_flag and reacted_to_upvote:
            post.flag_react.add(user)

        # Redirect to the post detail view
        return HttpResponseRedirect(reverse('post-detail', args=[str(post.id)]))


@method_decorator(login_required, name='dispatch')
class GuestReactView(View):
    def post(self, request, pk):
        post = get_object_or_404(GuestPost, pk=pk)
        user = request.user

        reacted_to_flag = False
        reacted_to_upvote = False

        # Check if the user has reacted to flag_react
        if post.flag_react.filter(id=user.id).exists():
            post.flag_react.remove(user)
            reacted_to_flag = True

        # Check if the user has reacted to upvote_react
        if post.upvote_react.filter(id=user.id).exists():
            post.upvote_react.remove(user)
            reacted_to_upvote = True

        # If the user hasn't reacted to flag_react 
        # and clicked the flag icon, add their reaction to flag_react
        if not reacted_to_flag and not reacted_to_upvote:
            post.flag_react.add(user)

        # If the user has already reacted to flag_react 
        # and clicked the upvote icon, add their reaction to upvote_react
        elif reacted_to_flag and not reacted_to_upvote:
            post.upvote_react.add(user)

        # If the user has already reacted to upvote_react 
        # and clicked the flag icon, add their reaction to flag_react
        elif not reacted_to_flag and reacted_to_upvote:
            post.flag_react.add(user)

        # Redirect to the post detail view
        return HttpResponseRedirect(reverse('guest-post-detail', args=[str(post.id)]))


class PostListView(ListView):
    model = CombinedPost
    template_name = 'concerns/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # Get all the posts and guest posts
        post_queryset = Post.objects.all()
        guest_post_queryset = GuestPost.objects.all()

        # Combine the posts and guest posts into a single list
        combined_posts = []
        for post in post_queryset:
            combined_posts.append(CombinedPost(post=post))
        for guest_post in guest_post_queryset:
            combined_posts.append(CombinedPost(guest_post=guest_post))

        # Sort the combined posts based on the desired criteria
        sort_param = self.request.GET.get('sort')  # Get the sort parameter from the request
        if sort_param == 'flags':
            combined_posts.sort(key=lambda post: post.total_flags(), reverse=True)
        elif sort_param == 'upvotes':
            combined_posts.sort(key=lambda post: post.total_upvotes(), reverse=True)
        else:
            combined_posts.sort(key=lambda post: post.get_latest_date(), reverse=True)
        return combined_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_ids = [post.post.id if post.post else post.guest_post.id for post in context['posts']]
        total_reactions = CombinedPost.objects.filter(
            Q(post__id__in=post_ids) | Q(guest_post__id__in=post_ids)
        ).annotate(
            total_upvotes=Count('post__upvote_react', distinct=True) + Count('guest_post__upvote_react', distinct=True),
            total_flags=Count('post__flag_react', distinct=True) + Count('guest_post__flag_react', distinct=True)
        ).values('id', 'total_upvotes', 'total_flags')
        context['total_reactions'] = {reaction['id']: {
            'total_upvotes': reaction['total_upvotes'],
            'total_flags': reaction['total_flags']
        } for reaction in total_reactions}
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'concerns/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['profile_user'] = user

        post_ids = context['posts'].values_list('id', flat=True)
        total_upvotes = Post.objects.filter(id__in=post_ids).annotate(
            total_upvotes=Count('upvote_react')).values('id', 'total_upvotes')
        total_flags = Post.objects.filter(id__in=post_ids).annotate(
            total_flags=Count('flag_react')).values('id', 'total_flags')
        upvote_counts = {item['id']: item['total_upvotes'] for item in total_upvotes}
        flag_counts = {item['id']: item['total_flags'] for item in total_flags}

        # Add the upvote_counts and flag_counts to the existing context dictionary
        context['upvote_counts'] = upvote_counts
        context['flag_counts'] = flag_counts
        return context 


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()
        total_upvotes = post.total_upvotes()
        total_flags = post.total_flags()

        reacted = False
        if post.upvote_react.filter(id=self.request.user.id).exists():
            reacted = True
        elif post.flag_react.filter(id=self.request.user.id).exists():
            reacted = True

        context['total_upvotes'] = total_upvotes
        context['total_flags'] = total_flags
        context['reacted'] = reacted
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['location','post_img','content']

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user 
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('profile')

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False


# Guest Post Views
class GuestPostCreateView(CreateView):
    model = GuestPost
    fields = ['email','phone_number','location','post_img','content']

    def get_success_url(self):
        return reverse_lazy('post-list')


class GuestPostDetailView(DetailView):
    model = GuestPost

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)

        fetch = get_object_or_404(GuestPost,id=self.kwargs['pk'])
        total_upvotes = fetch.total_upvotes()
        total_flags = fetch.total_flags()

        reacted = False
        if fetch.upvote_react.filter(id=self.request.user.id).exists():
            reacted = True
        elif fetch.flag_react.filter(id=self.request.user.id).exists():
            reacted = True

        context['total_upvotes'] = total_upvotes
        context['total_flags'] = total_flags
        context['reacted'] =  reacted
        return context