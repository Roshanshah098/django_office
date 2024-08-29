from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone  # Import timezone
from .models import Author, Reader, Post, PostAnalysis, PostView, Comment
from .serializers import (
    AuthorSerializer,
    ReaderSerializer,
    PostSerializer,
    PostAnalysisSerializer,
    PostViewSerializer,
    CommentSerializer,
)
from .managers import IsAuthor, IsReader
from django_filters import rest_framework as filters


class PostFilter(filters.FilterSet):
    author_name = filters.CharFilter(
        field_name="author__user__username", lookup_expr="icontains"
    )
    title = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ["author_name", "title"]


class AuthorViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthor]


class ReaderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsReader]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    authentication_classes = [BasicAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostFilter

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            self.permission_classes = [IsAuthor]
        else:
            self.permission_classes = [IsReader]
        return super().get_permissions()

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        ip_address = self.get_client_ip(request)

        viewer = None
        if request.user.is_authenticated and hasattr(request.user, "reader_profile"):
            viewer = request.user.reader_profile

        post_view, created = PostView.objects.get_or_create(
            post=post,
            ip_address=ip_address,
            viewer=viewer,
        )

        if not created:
            post_view.view_date = timezone.now()
            post_view.save()

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        if request.user.is_authenticated and hasattr(request.user, "reader_profile"):
            post.analysis.likes.add(request.user.reader_profile)
            post.save()
            return Response({"status": "post liked"})
        return Response({"error": "User not authenticated"}, status=401)

    @action(detail=True, methods=["post"])
    def dislike(self, request, pk=None):
        post = self.get_object()
        if request.user.is_authenticated and hasattr(request.user, "reader_profile"):
            post.analysis.likes.remove(request.user.reader_profile)
            post.save()
            return Response({"status": "post disliked"})
        return Response({"error": "User not authenticated"}, status=401)

    @action(detail=True, methods=["post"], url_path="rate")
    def rate_post(self, request, pk=None):
        post = self.get_object()
        rating = request.data.get("rating")

        serializer = PostAnalysisSerializer(
            post.analysis, data={"rating": rating}, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "post rating updated"})
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"], url_path="comment")
    def comment_on_post(self, request, pk=None):
        post = self.get_object()
        content = request.data.get("content")
        if not content:
            return Response({"error": "Content cannot be empty"}, status=400)

        Comment.objects.create(
            post=post, author=request.user.reader_profile, content=content
        )
        return Response({"status": "comment added"})

    @action(detail=False, url_path="recent")
    def recent_posts(self, request):
        recent_posts = Post.objects.all().order_by("-published_date")[:10]
        serializer = self.get_serializer(recent_posts, many=True)
        return Response(serializer.data)


# class PostViewViewSet(viewsets.ModelViewSet):
#     queryset = PostView.objects.all()  # Add queryset
#     serializer_class = PostViewSerializer
