from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from account.forms import SignUpForm
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post, Category
# Create your views here.

class SignUpView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return

class UserDetailsView(LoginRequiredMixin,DetailView):
    login_url = reverse_lazy('login')
    model = get_user_model()
    template_name = "profile/profile.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        user = self.get_object()
        posts = Post.objects.filter(author = user)
        for post in posts:
            print(post.author)
            print(self.request.user)
        context['categories'] = categories
        context['posts'] = posts
        return context


class UserUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = reverse_lazy("login")
    model = get_user_model()
    fields = ['first_name','last_name','email','pic','bio','groups']
    # form_class = SignUpForm
    pk_url_kwarg = 'id'
    template_name = "registration/signup.html"
    
    def test_func(self,*args, **kwargs):
        user = get_user_model().objects.get(id = self.kwargs.get('id'))
        print(user)
        if user == self.request.user:
            return True
        else:
            return False

class UserDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = reverse_lazy('login')
    model = get_user_model()
    template_name = "profile/confirm-delete.html" 
    success_url = reverse_lazy("home")
    pk_url_kwarg = 'id'

    def test_func(self,*args, **kwargs):
        user = get_user_model().objects.get(id = self.kwargs.get('id'))
        print(user)
        if user == self.request.user:
            return True
        else:
            return False