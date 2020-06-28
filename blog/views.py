from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from blog.models import Post,Category
from blog.forms import ContactUsForm, RegisterForm, PostForm
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

def post_details(request,id):
    post = Post.objects.get(id = id)
    cat = post.category
    return render(request, 'blog/blog-post.html', context = {'post':post,'cat':cat})

class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.filter(status = 'P')
    template_name = "blog/blog-post.html"
    pk_url_kwarg = 'id'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post = kwargs.get('object')
        cat = post.category
        context['cat'] = cat
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if not request.session.get('count'):
                request.session['count'] = 1
            else:
                request.session['count'] +=1
            if request.session.get('count') >3:
                return redirect(reverse_lazy("login"))
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

def category_specific(request,id):
    categories = Category.objects.all()
    posts = Post.objects.filter(category = id, status = "P")
    return render(request,'blog/stories.html',context = {'posts':posts, 'categories':categories})
def index(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(status = 'P')
    return render(request,'blog/stories.html',context = {'posts':posts, 'categories':categories})

class PostlistView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status = 'P')
    context_object_name = 'posts'
    template_name = "blog/stories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context



class ContactUsView(generic.FormView):
    form_class = ContactUsForm
    template_name = "blog/contact-us.html"
    success_url = reverse_lazy('success')

class SuccessView(generic.TemplateView):
    template_name = "blog/success-response.html"



class PostCreateView( LoginRequiredMixin, PermissionRequiredMixin ,generic.CreateView):
    permission_required = 'blog.add_post'
    login_url = reverse_lazy("login")
    model = Post
    form_class = PostForm
    template_name = "blog/post.html"
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UserPassesTestMixin,generic.UpdateView):
    permission_required = 'blog.change_post'
    login_url = reverse_lazy("login")
    model = Post
    fields = ['title', 'content', 'status', 'category', 'image']
    pk_url_kwarg = 'id'
    template_name = "blog/post.html"

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self,*args, **kwargs):
        post = Post.objects.get(slug = self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin,PermissionRequiredMixin,generic.DeleteView):
    permission_required = 'blog.delete_post'
    login_url = reverse_lazy("login")
    model = Post
    template_name = "blog/confirm-delete.html"
    success_url = reverse_lazy("home")

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self,*args, **kwargs):
        post = Post.objects.get(slug = self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False

class SearchView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = "blog/stories.html"
    def get_queryset(self, **kwargs):
        queryset1 = Post.objects.filter(status = 'P')
        queryset = queryset1.filter(Q(title__contains= self.request.GET.get('search')))
        print(self.request.GET.get('search'))
        print(queryset)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context
