# urls.py file for : function-based Views 
"""
from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),
]

#changing file for : Tutorial 2: Requests and Responses
#Adding optional format suffixes to our URLs

from rest_framework.urlpatterns import format_suffix_patterns
urlpatterns = format_suffix_patterns(urlpatterns)

"""
# test codes for : function-based Views
# with using : pip install httpie 
"""
#We can control the format of the response that we get back, either by using the Accept header:

http http://127.0.0.1:8000/snippets/ Accept:application/json  # Request JSON
http http://127.0.0.1:8000/snippets/ Accept:text/html         # Request HTML

http http://127.0.0.1:8000/snippets.json  # JSON suffix
http http://127.0.0.1:8000/snippets.api   # Browsable API suffix

#we can control the format of the request that we send, using the Content-Type header:

#POST using form data
http --form POST http://127.0.0.1:8000/snippets/ code="print(123)"

#POST using JSON
http --json POST http://127.0.0.1:8000/snippets/ code="print(456)"

"""

# urls.py file for : Class-based Views
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    #Tutorial 5: Relationships & Hyperlinked APIs
    path('', views.api_root),
    path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
"""

# Tutorial 5: Relationships & Hyperlinked APIs
# Making sure our URL patterns are named
# If we're going to have a hyperlinked API, we need to make sure we name our URL patterns
# which URL patterns we need to name:

    # The root of our API refers to 'user-list' and 'snippet-list'.
    # Our snippet serializer includes a field that refers to 'snippet-highlight'.
    # Our user serializer includes a field that refers to 'snippet-detail'.
    # Our snippet and user serializers include 'url' fields that by default will refer to '{model_name}-detail',
    # which in this case will be 'snippet-detail' and 'user-detail'.

# After adding all those names into our URLconf, 
# our final snippets/urls.py file should look like this:

"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('', views.api_root),
    path('snippets/',
        views.SnippetList.as_view(),
        name='snippet-list'),
    path('snippets/<int:pk>/',
        views.SnippetDetail.as_view(),
        name='snippet-detail'),
    path('snippets/<int:pk>/highlight/',
        views.SnippetHighlight.as_view(),
        name='snippet-highlight'),
    path('users/',
        views.UserList.as_view(),
        name='user-list'),
    path('users/<int:pk>/',
        views.UserDetail.as_view(),
        name='user-detail')
])
"""

# Tutorial 6: ViewSets & Routers
# Binding ViewSets to URLs explicitly
# The handler methods only get bound to the actions when we define the URLConf.
# To see what's going on under the hood let's first explicitly create a set of views from our ViewSets.
# we bind our ViewSet classes into a set of concrete views:
"""
from snippets.views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

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

# Notice how we're creating multiple views from each ViewSet class, 
# by binding the http methods to the required action for each view
# Now that we've bound our resources into concrete views, 
# we can register the views with the URL conf as usual:

urlpatterns = format_suffix_patterns([
    path('', api_root),
    path('snippets/', snippet_list, name='snippet-list'),
    path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail')
])

"""

# Tutorial 6: ViewSets & Routers
# Using Routers
# Because we're using ViewSet classes rather than View classes, 
# we actually don't need to design the URL conf ourselves.
# The conventions for wiring up resources into views and urls 
# can be handled automatically, using a Router class. 
# All we need to do is register the appropriate view sets with a router, and let it do the rest.
# Here's our re-wired snippets/urls.py file.

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from snippets import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]

# Registering the viewsets with the router is similar to providing a urlpattern. 
# We include two arguments - the URL prefix for the views, and the viewset itself.
# The DefaultRouter class we're using also automatically creates the API root view for us, 
# so we can now delete the api_root method from our views module.