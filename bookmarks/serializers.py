from .models import List, Bookmark
from rest_framework import serializers

class BookmarkSerializer(serializers.ModelSerializer):
    _list = serializers.SlugRelatedField(many=False, read_only=True, slug_field='url_id')

    class Meta:
        model = Bookmark
        fields = '__all__'
        
class ListSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True, read_only=True)

    class Meta:
        model = List
        exclude = ['id', 'owner']