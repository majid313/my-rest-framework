from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

"""serializer class similar to Django's forms classes
this class is replicating a lot of information that's also contained in the Snippet model

class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
    
       # Create and return a new `Snippet` instance, given the validated data.
    
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
    
        #Update and return an existing `Snippet` instance, given the validated data.
    
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance
"""

#serializer class similar to Django's ModelForm classes
#ModelSerializer classes are simply a shortcut for creating serializer classes
            #An automatically determined set of fields.
            #Simple default implementations for the create() and update() methods.
""" 
class SnippetSerializer(serializers.ModelSerializer):
    # Tutorial 4: Authentication & Permissions
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language', 'style']


# Tutorial 4: Authentication & Permissions
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
    
"""

from django.contrib.auth.models import User
#Tutorial 5: Relationships & Hyperlinked APIs
#Hyperlinking our API
# There are a number of different ways that we might choose to represent a relationship in  Web API design:

    #Using primary keys.
    #Using hyperlinking between entities.
    #Using a unique identifying slug field on the related entity.
    #Using the default string representation of the related entity.
    #Nesting the related entity inside the parent representation.
    #Some other custom representation.

#REST framework supports all of these styles
#and can apply them across forward or reverse relationships
#or apply them across custom managers such as generic foreign keys

#we'll modify our serializers to extend HyperlinkedModelSerializer instead of the existing ModelSerializer
#The HyperlinkedModelSerializer has the following differences from ModelSerializer:

    #It does not include the id field by default.
    #It includes a url field, using HyperlinkedIdentityField.
    #Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.

#We can re-write our existing serializers to use hyperlinking:

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    #'highlight' field points to the 'snippet-highlight' url pattern, instead of the 'snippet-detail' url pattern
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']