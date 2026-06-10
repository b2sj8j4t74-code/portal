from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import News
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly
from .serializers import NewsSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def perform_create(self, serializer):
        serializer.save()


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-date_created')
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['author']
    ordering_fields = ['date_created', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
