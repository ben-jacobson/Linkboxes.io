from django.db import models

# Create your models here.

'''
Models definition for Bookmarks

User (ID, manyToOne relationships with BookmarksList)
BookmarksList (Url, manyToOne relationships with links, Privacy flag, pin_code_for_editing)
Bookmarks (Title, URL, Picture URL)


User can have multiple bookmark lists - ManyToOne relationships
Lists can have multiple bookmarks - ManyToOne relationships
Bookmarks are the most granular component
'''

