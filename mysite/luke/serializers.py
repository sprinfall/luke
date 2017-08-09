from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Profile, Post, Photo, Tag, Visit


class ProfileSerializer(serializers.ModelSerializer):
    """
    ProfileSerializer will be nested into UserSerializer, don't use
    HyperlinkedModelSerializer.
    """

    class Meta:
        model = Profile

        # TODO: id
        fields = ('avatar', 'gender', 'birth_date', 'intro', 'city', 'country')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Django provides the following user fields:
    - username (Unique)
    - password (R)
    - email (O)
    - first_name (O)
    - last_name (O)
    - ...
    username is unique, password is required, others are all optional.
    For our app, first_name and last_name won't be used, so just ignore them.
    """

    # API hyperlinking to profile.
    # profile = serializers.HyperlinkedRelatedField(many=False,
    #                                               view_name='userprofile-detail',
    #                                               read_only=True)
    # Nested profile.
    # http://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
    profile = ProfileSerializer()


    class Meta:
        model = User

        # TODO: Django will check if the username is unique.
        fields = ('url', 'id', 'username', 'password', 'email', 'is_staff', 'profile')

        # Don't expose 'password'.
        # NOTE: write_only_fields has been deprecated:
        #     write_only_fields = ('password',)
        # extra_kwargs is the new way.
        # See: http://www.django-rest-framework.org/topics/3.0-announcement/#the-extra_kwargs-option
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        """
        Override create so that the password will be encrypted.
        See: https://stackoverflow.com/a/29748569
        """

        profile_data = validated_data.pop('profile')

        # TODO: create() or create_user()?
        # user = User.objects.create(**validated_data)
        user = User.objects.create_user(**validated_data)

        # The following implementation is from:
        # http://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
        # user = User(
        #     email=validated_data['email'],
        #     username=validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        # user.save()

        Profile.objects.create(user=user, **profile_data)

        return user


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('url', 'id', 'name')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    # TODO: user = UserSerializer(required=False)
    user = serializers.ReadOnlyField(source='user.username')

    photos = serializers.HyperlinkedIdentityField(view_name='postphoto-list', read_only=True)

    # TODO
    # Nest tags into post.
    #tags = TagSerializer(many=True, read_only=True)
    # Hyper links to tags.
    #tags = serializers.HyperlinkedRelatedField(many=True, view_name='tag-detail', read_only=True)

    class Meta:
        model = Post

        fields = ('url', 'id', 'user',
                  'content', 'create_time', 'last_update_time',
                  'mode', 'address', 'photos', 'tags')


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo

        fields = ('url', 'id', 'image', 'order')


class VisitSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Visit

        fields = ('url', 'id', 'user', 'timestamp', 'state')
