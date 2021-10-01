from rest_framework import serializers

from account.models import User
from twister.models import Publication, Comment, Likes, Rating, Favorites


class PublicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('id',  'text', 'user')


class PublicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
            return rep


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CreatePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    publication = serializers.PrimaryKeyRelatedField(write_only=True,
                                                     queryset=Publication.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'publication', 'text', 'user')


class CreatePublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        ads = validated_data.get('ads')

        if Likes.objects.filter(author=user, ads=ads):
            return Likes.objects.get(author=user, ads=ads)
        else:
            return Likes.objects.create(author=user, ads=ads)


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'ads')

    def create(self, validated_data):
        request = self.context.get('request')
        rating, user = Rating.objects.update_or_create(
            ads=validated_data.get('ads', None),
            author=request.user,
            star=validated_data.get("star", None)
        )
        return rating


class FavoriteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Favorites
        fields = ('id', 'publication', 'name', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')

        if action == 'list':
            representation['publication'] = instance.publication.name

        elif action == 'retrieve':
            representation['publication'] = PublicationListSerializer(instance.post).data

        return representation

    def create(self, validated_data):
        request = self.context.get('request')

        if Favorites.objects.filter(post=validated_data.get('publication'), author=validated_data.get('author')):
            raise serializers.ValidationError('This publication has already been added to favorites.')

        favorites = Favorites.objects.create(
            **validated_data
        )

        return favorites
