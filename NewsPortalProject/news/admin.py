from django.contrib import admin
from .models import Post, Category, Author, Comment, PostCategory
from modeltranslation.admin import TranslationAdmin


class TransCategoryAdmin(TranslationAdmin):
    model = Category


class TransPostAdmin(TranslationAdmin):
    model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('date', 'heading', 'author', 'rating')
    list_filter = ('date', 'author', 'rating')
    search_fields = ('author__user__username', 'rating', 'heading', 'text')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user__username', 'rating')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('category__name', )
    search_fields = ('category__name', 'post__author__user__username')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment)
