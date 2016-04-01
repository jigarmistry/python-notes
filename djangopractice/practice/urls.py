from django.conf.urls import url
from .views import PublisherList, AuthorCreate, AuthorUpdate, AuthorDelete,PostView ,post_detail,api_response,api_list,project_list

app_name = 'practice'

urlpatterns = [
    url(r'^publishers/$', PublisherList.as_view()),
    url(r'^posts/$', PostView.as_view(), name='posts'),
    url(r'^post/(?P<pk>[0-9]+)/$', post_detail, name='post_detail'),
    url(r'author/add/$', AuthorCreate.as_view(), name='author-add'),
    url(r'author/(?P<pk>[0-9]+)/$', AuthorUpdate.as_view(), name='author-update'),
    url(r'author/(?P<pk>[0-9]+)/delete/$', AuthorDelete.as_view(), name='author-delete'),

    url(r'^api/(?P<project_name>\w+)/(?P<api_name>\w+)$', api_response, name='api_response'),
    url(r'^api/(?P<project_name>\w+)/$', api_list, name='api_list'),
    url(r'^api/$', project_list ,name='projects'),
]
