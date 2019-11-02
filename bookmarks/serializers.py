from .models import List, Bookmark
from rest_framework import serializers

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        exclude = ['_list']

class ListSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True)

    class Meta:
        model = List
        exclude = ['owner']
