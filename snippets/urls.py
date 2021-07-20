from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from snippets.views import SnippetViewSet, UserViewSet, api_root


# Urls using ViewSets.
# Because multiple views from each ViewSet are being created, is necessary to
# bind the http methods to the required action for each view.
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# Now the views are registered as usual.
urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])


'''
from collections import namedtuple
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views


# Urls using class-based views.
urlpatterns = [
    path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', views.SnippetHighLight.as_view(), name='snippet-highlight'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
'''

''' Urls using methods based views.
urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail)
]
'''


'''
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Urls using Router
# Create a router and register our viewsets with it.
# Registering the viewsets with the router is similar to providing a urlpattern
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Because the DefaultRouter class automatically creates the API root view, 
# we can delete the api_root method from the views module.
'''
