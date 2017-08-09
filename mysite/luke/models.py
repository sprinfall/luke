from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


################################################################################


class Profile(models.Model):
    """
    Profile of user.
    Profile will be created automatically on user creation.
    TODO: ordering
    """

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )

    # Using related_name yo u can access a user's profile easily, for example
    # for request.user
    #     request.user.profile.location
    #     request.user.profile.gender
    # No need for additional lookups.
    # See: https://stackoverflow.com/a/37348787
    # NOTE: Use user_id as the primary key.
    user = models.OneToOneField(User, primary_key=True, related_name='profile')

    # Profile picture.
    avatar = models.ImageField(upload_to='avatar', max_length=255, null=True, blank=True)

    gender = models.CharField(max_length=1, choices=GENDERS, default='U')

    birth_date = models.DateField(null=True)

    # Self introducation (normally one sentence).
    intro = models.CharField(max_length=100, default='', blank=True)

    city = models.CharField(max_length=30, default='', blank=True)
    country = models.CharField(max_length=30, default='', blank=True)

    # Cell phone number.
    # phone = models.CharField(max_length=

    # wechat = models.CharField(max_length=30, default='', blank=True)

    # level = models

    def __str__(self):
        return 'Profile: {}'.format(self.user.username)


# Use signal to automatically create user profile on user creation.
# See: https://stackoverflow.com/q/1910359
#
# NOTE: Don't do this in a separate file (e.g., signals.py) or the signal
# will not be connected.
#
# Another implementation:
# def create_user_profile(sender, **kwargs):
#     user = kwargs["instance"]
#     if kwargs["created"]:
#         ...
def create_user_profile(sender, instance, created, **kwargs):
    """
    :param sender: Class User.
    :param instance: The user instance.
    """
    if created:
        # Seems the following also works:
        #   UserProfile.objects.create(user=instance)
        # TODO: Which is better?
        profile = Profile(user=instance)
        profile.save()

# NOTE: Comment to nest profile into user.
# post_save.connect(create_user_profile,
#                   sender=User,
#                   dispatch_uid="users-profilecreation-signal")


################################################################################


class Tag(models.Model):
    """
    TODO: ordering
    """

    name = models.CharField(max_length=32)

    def __str__(self):
        return 'Tag: {}'.format(self.name)


################################################################################


class Post(models.Model):

    class Meta:
        ordering = ('create_time',)

    # Happy, Sad, etc.
    MODES = (
        ('', 'Normal'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        # TODO
    )

    # The user who created this message.
    # The first parameter could also be string "auth.User".
    # TODO: Use get_user_model() instead of User.
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    content = models.CharField(max_length=256)

    create_time = models.DateTimeField(auto_now_add=True)

    last_update_time = models.DateTimeField(auto_now_add=True)

    mode = models.CharField(max_length=16, choices=MODES, default='')

    # TODO
    # Optional
    # Rename to location
    address = models.CharField(max_length=256, default='')

    # A post has multiple tags.
    # A tag belongs to multiple posts.
    tags = models.ManyToManyField(Tag)

    # A post can be visited by many users.
    # The user may Like, Dislike or just Do Nothing about the post.
    visits = models.ManyToManyField(User, through='Visit')

    def __str__(self):
        # TODO
        return 'Post: {}'.format(self.content)


################################################################################


class Photo(models.Model):

    # A post has multiple photos.
    post = models.ForeignKey(Post, related_name='photos', on_delete=models.CASCADE)

    # TODO: upload_to='%Y/%m/%d'
    image = models.ImageField(upload_to='post_photos')

    # For ordering: 1, 2, 3, etc.
    order = models.SmallIntegerField(default=0)


################################################################################


class Visit(models.Model):
    """
    See this discussion: https://stackoverflow.com/q/21919422
    """

    STATES = (
        (0, 'None'),
        (1, 'Like'),
        (2, 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    state = models.SmallIntegerField(choices=STATES, default=0)
