# Serializers allow complex data such as querysets and model instances to be converted
# to native Python datatypes that can then be easily rendered into JSON, XML or other
# content types. Serializers also provide deserialization, allowing parsed data to be
# converted back into complex types, after first validating the incoming data.

from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet  # , LANGUAGE_CHOICES, STYLE_CHOICES

'''
class SnippetSerializer(serializers.Serializer):
    # Fields that get serialized/deserialized.
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    # Create and return a new Snipped instance, given the validated data.
    def create(self, validated_data):
        return Snippet.objects.create(**validated_data)

    # Update and return an existing Snippet instance, given the validated data.
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()

        return instance
'''


'''
# The implementation of SnippetSerializer above is replicating a lot of information that
# is also contained in the Snippet Model.
# ModelSerializer shortcuts the creation of a serializer class by:
# - Automatically determining set of fields;
# - Simple implementations by default for the create() and update() methods.
class SnippetSerializer(serializers.ModelSerializer):
    # The untyped ReadOnlyField is always read-only, and will be used for serialized
    # representations, but will not be used for updating model instances when they are deserialized. 
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.ModelSerializer):
    # Because 'snippets' is a reverse relationship on the User model, it will not be included by
    # default when using the ModelSerializer class, so we needed to add an explicit field for it.
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
'''


# The HyperlinkedModelSerializer has the following differences from ModelSerializer:
# - It does not include the id field by default.
# - It includes a url field, using HyperlinkedIdentityField.
# - Relationships use HyperlinkedRelatedField, instead of PrimaryKeyRelatedField.
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ['id', 'owner', 'title', 'code', 'linenos', 'language', 'style', 'url', 'highlight',]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets', 'url']
