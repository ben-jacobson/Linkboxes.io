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

class BookmarksList(models.Model):
    title = models.CharField(max_length=512, blank=False)
    # Todo - insert User Foreign Key

class Bookmark(models.Model):
    title = models.CharField(max_length=512, blank=False)
    thumbnail_url = models.CharField(max_length=2048)
    url = models.CharField(max_length=2048, blank=False)
    bookmarks_list = models.ForeignKey(BookmarksList, on_delete=models.CASCADE, related_name='bookmarks_list')     # ManyToOne - BookmarksList can have multiple BookMarks, but a BookMark can only be associated with one list. 

    def save(self, *args, **kwargs):
        if self.thumbnail_url == '':
            self.thumbnail_url = '/no_thumbnail.jpg'        # for some reason, plugging in default= into the model.Charfield didn't work..
        super(Bookmark, self).save(*args, **kwargs)