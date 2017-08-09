import logging

from django.contrib.auth.models import User

from rest_framework import generics, views
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework.parsers import FileUploadParser

from .models import Profile, Tag, Post, Photo, Visit
from .serializers import TagSerializer, PostSerializer, PhotoSerializer, VisitSerializer
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwnerOrReadOnly, IsThisUserOrReadOnly


logger = logging.getLogger('luke')


# NOTE: Don't use View Set, it hides too much.


################################################################################
# Root View
################################################################################


@api_view(['GET'])
def api_root(request, format=None):
    """
    Root endpoint of our API.
    """
    return Response({
        # 1. Use reverse function in order to return fully-qualified URLs;
        # 2. URL patterns are identified by convenience names declared in urls.py.
        'users': reverse('user-list', request=request, format=format),
        'tags': reverse('tag-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format),
        'photos': reverse('photo-list', request=request, format=format),
        'visits': reverse('visit-list', request=request, format=format)
    })


################################################################################
# User & Profile Views
################################################################################


class UserList(generics.ListCreateAPIView):
    """
    List users or create a new user.

    List users:
        $ http :8000/users/
    Create a user:
        $ http POST :8000/users/ username="test" password="123456" profile:='{"gender": "M", "city": "Shanghai"}'
        (username and password are required, email is optional)
    TODO: User creation should be restricted.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Override get_permissions instead of setting permission_classes so that
        we can specify different permissions for different HTTP methods.
        """

        if self.request.method == "GET":
            return [permissions.IsAdminUser()]
        else:  # POST
            return [permissions.AllowAny()]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an user.

    Retrieve an user:
        $ http http://127.0.0.1:8000/users/1/
    Update an user:
        $ http -a <name>:<pw> PUT http://127.0.0.1:8000/users/2/ username="new_name" password="new_pw"
        (All required fields must be provided.)
    Partial update a user:
        $ http -a <name>:<pw> PATCH http://127.0.0.1:8000/users/2/ username="new_name"
    Delete an user:
        $ http -a <admin>:<pw> DELETE http://127.0.0.1:8000/users/2/
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'DELETE':
            return [permissions.IsAdminUser()]
        else:  # PUT, PATCH (Update)
            return [permissions.IsAdminUser(), IsThisUserOrReadOnly()]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


# class UserProfileList(generics.ListCreateAPIView):
#
#     queryset = Profile.objects.all()
#     serializer_class = UserProfileSerializer
#
#     # Any authenticated user can create new tags.
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class UserProfileDetail(generics.RetrieveUpdateAPIView):
#
#     queryset = Profile.objects.all()
#     serializer_class = UserProfileSerializer
#
#     # Only the user itself can update.
#     # TODO
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly)


# class UserAvatarView(generics.CreateAPIView):
#
#     parser_classes = (FileUploadParser,)
#
#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#         # do some stuff with uploaded file
#         # ...
#         return Response(status=status.HTTP_201_CREATED)


################################################################################
# Tag Views
################################################################################


class TagList(generics.ListCreateAPIView):
    """
    List all tags, or create a new tag.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    # Any authenticated user can create new tags.
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TagDetail(generics.RetrieveAPIView):
    """
    Retrieve a tag.
    No need to update or destroy a tag.
    The system will clean up unused tags periodically.
    TODO
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


################################################################################
# Post Views
################################################################################


class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # TODO: Remove IsOwnerOrReadOnly
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class PostPhotoList(generics.ListAPIView):
    """
    List the photos of a post.
    """

    model = Photo
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        queryset = super(PostPhotoList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))


# TODO
class PostTagList(generics.ListAPIView):
    model = Tag
    serializer_class = TagSerializer

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        queryset = post.tags
        return queryset


################################################################################
# Photo Views
################################################################################


class PhotoList(generics.ListCreateAPIView):
    """
    Create/upload a photo:
    $ http -a username:password -f POST :8000/photos/ image@~/test.jpg
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class PhotoDetail(generics.RetrieveDestroyAPIView):
    """
    Delete a photo (TODO: Also delete the image file from disk):
    $ http -a username:password -v DELETE :8000/photos/2/
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# class PhotoUploadView(generics.CreateAPIView):
#     parser_classes = (FileUploadParser,)
#
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def perform_create(self, serializer):
#         file_obj = self.request.data['file']
#
#         self[]
#         # do some stuff with uploaded file
#
#         serializer.save(user=self.request.user)
#
#
#     def put(self, request, filename, format=None):
#         file_obj = request.data['file']
#         # ...
#
#         # ...
#         return Response(status=204)


# class PhotoUploadView(views.APIView):
#     parser_classes = (FileUploadParser,)
#
#     def post(self, request, format=None):
#         file = request.data['file']
#
#         logger.debug("upload file: {}".format(file.name))
#
#         return Response(status=204)


################################################################################
# Visit Views
################################################################################


class VisitList(generics.ListCreateAPIView):
    """
    List visits or create a new visit.
    """

    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VisitDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a visit.
    """

    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
