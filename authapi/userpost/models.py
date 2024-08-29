from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Constants for Choices
CHOOSE_ADDRESS = [
    ("ktm", "Kathmandu"),
    ("lat", "Lalitpur"),
    ("bat", "Bhaktapur"),
]

GENDER_CHOICES = [
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
]


# Author Model
class Author(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="author_profile", null=True
    )
    email = models.EmailField(max_length=50, unique=True, default="example@example.com")
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, default="images/default.jpg"
    )
    bio = models.TextField(null=True, blank=True, verbose_name="Biography")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="other")
    address = models.CharField(max_length=40, choices=CHOOSE_ADDRESS, default="ktm")

    def __str__(self):
        return self.user.username if self.user else "Unknown User"


# Reader Model
class Reader(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="reader_profile", null=True
    )
    email = models.EmailField(max_length=50, unique=True, default="example@example.com")
    image = models.ImageField(
        upload_to="images/", blank=True, null=True, default="images/default.jpg"
    )
    favorite_genre = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="other")
    address = models.CharField(max_length=40, choices=CHOOSE_ADDRESS, default="ktm")

    def __str__(self):
        return self.user.username if self.user else "Unknown User"


# Post Model
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Post Title")
    content = models.TextField(verbose_name="Content")
    published_date = models.DateTimeField(
        default=timezone.now, verbose_name="Published Date"
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    tags = models.CharField(max_length=100, blank=True, verbose_name="Tags")

    def __str__(self):
        return self.title


class PostAnalysis(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="analysis")

    # Post Rating
    rating = models.PositiveSmallIntegerField(verbose_name="Rating")

    # Post Likes
    likes = models.ManyToManyField(Reader, related_name="liked_posts", blank=True)

    def __str__(self):
        return f"Analysis for {self.post.title}"


# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        Reader, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Created At")

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.post.title}"


# Post View Model
class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="views")
    viewer = models.ForeignKey(
        Reader,
        on_delete=models.CASCADE,
        related_name="post_views",
        null=True,
        blank=True,
    )
    view_date = models.DateTimeField(default=timezone.now, verbose_name="View Date")
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        viewer_name = self.viewer.user.username if self.viewer else "Anonymous"
        return f"View by {viewer_name} on {self.post.title}"
