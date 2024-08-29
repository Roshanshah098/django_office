from rest_framework import serializers
from .models import Author, Reader, Post, PostAnalysis, Comment, PostView


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = "__all__"


class PostAnalysisSerializer(serializers.ModelSerializer):
    likes = ReaderSerializer(many=True, read_only=True)  # Serialize related reader data

    class Meta:
        model = PostAnalysis
        fields = ["rating", "likes"]

    def to_internal_value(self, data):
        # Start with the default validation
        validated_data = super().to_internal_value(data)

        # Ensure the rating is between 1 and 5
        rating = validated_data.get("rating")
        if rating < 1 or rating > 5:
            raise serializers.ValidationError(
                {"rating": "Rating must be between 1 and 5."}
            )

        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = ReaderSerializer(read_only=True)  # Serialize related reader data

    class Meta:
        model = Comment
        fields = ["post", "author", "content", "created_at"]


class PostViewSerializer(serializers.ModelSerializer):
    viewer = ReaderSerializer(read_only=True)  # Serialize related viewer data
    post = serializers.StringRelatedField()

    class Meta:
        model = PostView
        fields = ["post", "viewer", "view_date", "ip_address"]  # Included ip_address


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)  # Serialize related author data
    analysis = PostAnalysisSerializer(
        read_only=True
    )  # Serialize the related PostAnalysis data
    comments = CommentSerializer(
        many=True, read_only=True
    )  # Serialize related comments data
    views = PostViewSerializer(
        many=True, read_only=True
    )  # Serialize related views data

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published_date",
            "author",
            "analysis",
            "comments",
            "views",
            "tags",
        ]
