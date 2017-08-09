from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    url(r'^$', views.api_root),

    url(r'^tags/(?P<pk>\d+)/$', views.TagDetail.as_view(), name='tag-detail'),
    url(r'^tags/$', views.TagList.as_view(), name='tag-list'),

    url(r'^posts/$', views.PostList.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>\d+)/$', views.PostDetail.as_view(), name='post-detail'),
    url(r'^posts/(?P<pk>\d+)/photos/$', views.PostPhotoList.as_view(), name='postphoto-list'),
    url(r'^posts/(?P<pk>\d+)/tags/$', views.PostTagList.as_view(), name='posttag-list'),

    url(r'^photos/$', views.PhotoList.as_view(), name='photo-list'),
    url(r'^photos/(?P<pk>\d+)/$', views.PhotoDetail.as_view(), name='photo-detail'),

    url(r'^visits/$', views.VisitList.as_view(), name='visit-list'),
    url(r'^visits/(?P<pk>[0-9]+)/$', views.VisitDetail.as_view(), name='visit-detail'),

    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
    # url(r'^profiles/$', views.UserProfileList.as_view(), name='userprofile-list'),
    # url(r'^profiles/(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view(), name='userprofile-detail'),
]


# Suffix URL pattern examples:
# ^posts\.(?P<format>[a-z0-9]+)/?$
# ^posts/(?P<pk>[0-9]+)\.(?P<format>[a-z0-9]+)/?$
urlpatterns = format_suffix_patterns(urlpatterns)
