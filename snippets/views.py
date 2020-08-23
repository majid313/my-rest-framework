
#views.py file for : Tutorial 1: Serialization
"""
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Create your views here.
@csrf_exempt
def snippet_list(request):
    
    #List all code snippets, or create a new snippet.
    
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    
    #Retrieve, update or delete a code snippet.
    
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)

"""
#views.py file for : Tutorial 2: Requests and Responses
""" 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

@api_view(['GET','POST'])
def snippet_list(request, format=None):
    
    #List all code snippets, or create a new snippet.
    
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    
    #Retrieve, update or delete a code snippet.
    
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

#views.py file for : Tutorial 3: Class-based Views
"""
from snippets.serializers import SnippetSerializer
from snippets.models import Snippet
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class SnippetList(APIView):
    
    #List all snippets, or create a new snippet.
    
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SnippetDetail(APIView):
    
    #Retrieve, update or delete a code snippet.
    
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""

# views.py file for : Class-based Views
# with using REST framework's mixin classes
#The create/retrieve/update/delete operations are common behaviours
#and implemented in REST framework's mixin classes
"""
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # the list() function is form mixin class
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # the create() function is form mixin class
        return self.create(request, *args, **kwargs)


class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        # the retrieve() function is form mixin class
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # the update() function is form mixin class
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # the destroy() function is form mixin class
        return self.destroy(request, *args, **kwargs)

"""
# views.py file for :generic  Class-based Views
# with using REST framework's generic classes
#The create/retrieve/update/delete operations are common behaviours
#and implemented in REST framework's generic classes

"""
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import generics        
# Tutorial 4: Authentication & Permissions
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # Tutorial 4: Authentication & Permissions
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    # Tutorial 4: Authentication & Permissions
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

# Tutorial 4: Authentication & Permissions
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Tutorial 4: Authentication & Permissions; my test
    permission_classes = [permissions.IsAuthenticated]

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#Tutorial 5: Relationships & Hyperlinked APIs
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

#Creating an endpoint for the highlighted snippets
from rest_framework import renderers


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
"""

# Tutorial 6: ViewSets & Routers
# ViewSet classes are almost the same thing as View classes, 
# except that they provide operations such as read, or update, 
# and not method handlers such as get or put.

# Refactoring to use ViewSets
# refactor our UserList and UserDetail views into a single UserViewSet

from rest_framework import viewsets
from snippets.serializers import UserSerializer, SnippetSerializer
from django.contrib.auth.models import User
from snippets.models import Snippet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, renderers
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


# the ReadOnlyModelViewSet class automatically provide the default 'read-only' operations
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    
    #This viewset automatically provides `list` and `detail` actions.
    
    queryset = User.objects.all()
    serializer_class = UserSerializer



# replace the SnippetList, SnippetDetail and SnippetHighlight view classes
# We can remove the three views, and again replace them with a single class.
# the ModelViewSet class get the complete set of default read and write operations
class SnippetViewSet(viewsets.ModelViewSet):
    
    # This viewset automatically provides `list`, `create`, `retrieve`,
    # `update` and `destroy` actions.

    # Additionally we also provide an extra `highlight` action.
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    # used the @action decorator to create a custom action, named highlight
    # This decorator can be used to add any custom endpoints that don't fit
    # into the standard create/update/delete style.
    # Custom actions which use the @action decorator will respond to GET requests by default.
    # We can use the methods argument if we wanted an action that responded to POST requests.

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



# The DefaultRouter class (in snippets/urls.py file) we're using also automatically creates the API root view for us, 
# so we can now delete the api_root method from our views module.
"""
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })
"""