from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User 
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView, 
	UpdateView,
	DeleteView
)
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin   # we can't use @login_required on class as decorators can't be used on classes, so we use LoginRequiredMixin class

# Create your views here.



def home(request):
	context = {
		'posts' : Post.objects.all(),
		'title' : 'Nitesh Babu'
	}
	return render(request,'blog/home.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'     # template expects 'object' but we rename context_object = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
	context_object_name = 'posts'  		   # template expects 'object' but we rename context_object = 'posts'
	paginate_by = 5
	extra_context = {}

	def get_queryset(self):
		user = get_object_or_404(User, username = self.kwargs.get('username'))
		self.extra_context ={ 'author' : Post.objects.filter(author = user).last().author}
		return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post


class PostCreateView(LoginRequiredMixin, CreateView):  #LoginRequiredMixin should be the 1st param.
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title', 'content']
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False


def about(request):
	return render(request, 'blog/about.html',{'title' : 'About'})