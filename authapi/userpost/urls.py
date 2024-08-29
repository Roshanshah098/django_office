from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, ReaderViewSet, PostViewSet  # , PostViewViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")
router.register(r"readers", ReaderViewSet, basename="reader")
router.register(r"posts", PostViewSet, basename="post")
# router.register(r'post-views', PostViewViewSet, basename='post-views')

urlpatterns = [
    path("", include(router.urls)),  # Include the router URLs
    path(
        "auth/", include("rest_framework.urls", namespace="rest_framework")
    ),  # For session authentication
]
