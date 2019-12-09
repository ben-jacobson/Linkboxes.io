from django.db import models
from django.conf import settings

from datetime import datetime
from hashids import Hashids

#from django.core.exceptions import ValidationError

'''
Models definition for Bookmarks

User (ID, manyToOne relationships with List)
List (Url, manyToOne relationships with links, Privacy flag, pin_code_for_editing)
Bookmarks (Title, URL, Picture URL)

User can have multiple bookmark lists - ManyToOne relationships
Lists can have multiple bookmarks - ManyToOne relationships
Bookmarks are the most granular component
'''

def encode_url_id(encode_string):
    ### generate the hash
    date_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S:%f")           # start by creating a string of the date + time + milliseconds
    date_string += encode_string                                            # include the title
    hashids = Hashids(salt=date_string)                                     # make use of hashids to generate the id
    return hashids.encode(6, 666)                                           # encode it, 6's because hail satan    

class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='list_owner')
    title = models.CharField(max_length=512, blank=False)
    url_id = models.SlugField(max_length=5, blank=False, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # on creation, the bookmarks list needs to create a 5 digit tinyurl for the page. We don't want this to run on every save because that will re-roll your urls
        # the tinyurl should be unique, so the algorithm needs to ensure there is no clash
        # the algorithm used can be a string of the DD:MM:YYYY:HH:MM:SS:M + name of the page - made into a 5 digit hash
        # the algorithm allows for 60M+ different combinations from 00000 to zzzzz. We'll outgrow our database bandwidth well before we run out of bookmark lists 
        if not self.url_id:
            self.url_id = encode_url_id(self.title)
        
        ### checking for collision is automatic, because field is set to be unique so should raise an IntegrityError if any issues
        super(List, self).save(*args, **kwargs) 

    '''def reorder_bookmarks(self, related_bookmarks):
        pass

    def check_duplicate_bookmark_ordering(self):
        return False # pass for now

    def refresh_bookmark_ordering(self):
    '''
    # Helper function, called on model save, if the ordering bookmarks has changed at all, or is invalid, this function will re-order them.
    '''
        related_bookmarks = self.bookmarks.all()
        order_map = [] 

        # create an array of the ordering
        for bookmark in related_bookmarks:
            print(f'Before - {bookmark.order}: {bookmark.title}')
            order_map.append(bookmark.order)
        
            # on the way, if we encounter any zero orders, set a flag to re_order 
            if bookmark.order == 0: 
                self.reorder_bookmarks(related_bookmarks)

        # check if any duplicates in the values, if so - reorder
        if self.check_duplicate_bookmark_ordering() == True: ### #USE SET() if len(listOfElems) == len(set(listOfElems)):

            self.reorder_bookmarks(related_bookmarks)

        # Debug only - output the new ordering
        print('')
        for bookmark in related_bookmarks:
            print(f'After - {bookmark.order}: {bookmark.title}')'''

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    title = models.CharField(max_length=512, blank=False)
    thumbnail_url = models.CharField(max_length=2048, blank=True)
    url = models.CharField(max_length=2048)
    #order = models.PositiveIntegerField(default=0)    # determines which order does the bookmark appear on page? 
    _list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='bookmarks')     # ManyToOne - List can have multiple BookMarks, but a BookMark can only be associated with one list. 

    def save(self, *args, **kwargs):
        # insert the default thumbnail url
        if not self.thumbnail_url:
            self.thumbnail_url = '/no_thumbnail.jpg'        # for some reason, plugging in default= into the model.Charfield didn't work..
        super(Bookmark, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = '_list'
