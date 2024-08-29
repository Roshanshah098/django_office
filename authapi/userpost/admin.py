from django.contrib import admin
from .models import Author, Reader, Post, PostAnalysis, Comment, PostView


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "image", "bio", "gender", "address")
    search_fields = ("user__username", "email", "bio")
    list_filter = ("gender", "address")


@admin.register(Reader)
class ReaderAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "image", "favorite_genre", "gender", "address")
    search_fields = ("user__username", "email", "favorite_genre")
    list_filter = ("gender", "address")


class PostAnalysisInline(admin.StackedInline):
    model = PostAnalysis
    can_delete = False
    readonly_fields = ("likes_count",)

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = "Likes Count"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "tags")
    search_fields = ("title", "content", "author__user__username")
    list_filter = ("published_date", "author")
    date_hierarchy = "published_date"
    inlines = [PostAnalysisInline]


@admin.register(PostAnalysis)
class PostAnalysisAdmin(admin.ModelAdmin):
    list_display = ("post", "rating", "likes_count")
    search_fields = ("post__title",)
    list_filter = ("rating",)

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = "Likes Count"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "content", "created_at")
    search_fields = ("post__title", "author__user__username", "content")
    list_filter = ("created_at",)


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("post", "viewer", "view_date", "ip_address")
    search_fields = ("post__title", "viewer__user__username", "ip_address")
    list_filter = ("view_date",)
