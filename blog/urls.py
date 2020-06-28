from django.urls import path
from blog.views import index,post_details, category_specific
from blog.views import ContactUsView, PostlistView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, SuccessView, SearchView
urlpatterns = [
    path("", PostlistView.as_view(), name= 'home'),
    path("<int:id>", category_specific, name= 'category_specific'),
    path('blog/<slug:slug>', PostDetailView.as_view(), name= 'post-detail'),
    path('contact',ContactUsView.as_view(), name='contact'),
    path('post', PostCreateView.as_view(), name= 'create_new' ),
    path('post/<slug:slug>', PostUpdateView.as_view(), name= 'update_post'),
    path('post_delete/<slug:slug>', PostDeleteView.as_view(), name= 'delete_post'),
    path('success', SuccessView.as_view(), name='success'),
    path('url', SearchView.as_view(), name='search_page')
]