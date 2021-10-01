from django.shortcuts import render

from django_filters import rest_framework as filters
from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from twister.models import Publication, Comment, Likes, Rating, Favorites
from twister.permissions import IsAuthorOrIsAdmin, IsAuthor
from twister.serializers import CreatePublicationSerializer, PublicationListSerializer, \
    PublicationDetailSerializer, CommentSerializer, LikeSerializer, CreateRatingSerializer, \
    FavoriteSerializer
from rest_framework import filters as rest_filters


class PublicationFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Publication
        fields = ('status', 'created_at')


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = CreatePublicationSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = PublicationFilter
    search_fields = ['name', 'text']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicationListSerializer
        elif self.action == 'retrieve':
            return PublicationDetailSerializer
        return CreatePublicationSerializer


class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class UpdateCommentView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class DeleteCommentView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class LikesView(ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikeSerializer

    @action(detail=False, methods=['get'])
    def favorite(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = LikeSerializer(queryset, many=True,
                                    context={'request': request})
        return Response(serializer.data, status=200)


class AddStarRatingView(ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)


class FavoritesViewSet(ListModelMixin,
                       CreateModelMixin,
                       RetrieveModelMixin,
                       DestroyModelMixin,
                       GenericViewSet):

    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



