from django.contrib import admin
from blog.models import Post
from blog.models import Category
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','category','author','modified_date')
    search_fields = ('title','author','category')
    list_filter = ('status', 'category')
    select_related = ('category','author')
admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)