from django.db import models
from django.conf import settings

from datetime import datetime
from hashids import Hashids

#from django.core.exceptions import ValidationError

THUMBNAIL_IMAGE_HREF = 'https://bookmark-static.s3.amazonaws.com/no_thumbnail.jpg'

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
        # the algorithm used can be a string of the DD:MM:YYYY:HH:MM:SS:M + name of the page - made into a 5 digit hash        # the algorithm allows for 60M+ different combinations from 00000 to zzzzz. We'll outgrow our database bandwidth well before we run out of bookmark lists 
    
        if not self.url_id:
            self.url_id = encode_url_id(self.title)
        
        ### checking for collision is automatic, because field is set to be unique so should raise an IntegrityError if any issues
        super(List, self).save(*args, **kwargs) 

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    title = models.CharField(max_length=512, blank=False)
    thumbnail_url = models.CharField(max_length=2048, blank=True)
    url = models.CharField(max_length=2048)
    _list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='bookmarks')     # ManyToOne - List can have multiple BookMarks, but a BookMark can only be associated with one list. 

    def save(self, *args, **kwargs):
        # ensure that the url is prefixed with a '//'. Note that we don't need to specify http or https, we can let the browser decide
        if self.url and '//' not in self.url: # will only append if the user entered a url, because we dont want this code preventing validation errors from occuring when the user forgets to add their url
            self.url = '//' + self.url

        # insert the default thumbnail url
        if not self.thumbnail_url:
            self.thumbnail_url = THUMBNAIL_IMAGE_HREF        # for some reason, plugging in default= into the model.Charfield didn't work..
        super(Bookmark, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = '_list'
