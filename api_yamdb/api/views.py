from django.shortcuts import render
from rest_framework import viewsets

from .permissions import AuthorOrReadOnly
from .serializers import CommentSerializer, ReviewsSerializer
from reviews.models import Comment, Reviews

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        review_id = self.kwargs.get('id')
        return Comment.objects.filter(review=review_id)
