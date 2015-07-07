#don't forget to register models in admin
#!may have to delete db.sqlite3 and redo python manage.py syncdb after changing models
#   admin.site.register(model)
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
#http://www.cafepy.com/article/python_attributes_and_methods/python_attributes_and_methods.html#method-resolution-order
#http://stackoverflow.com/questions/7141820/use-of-python-super-function-in-django-model
        #i think this makes it so you use a 'save()' of something else, not category, and 'self' becomes the first arg
        #essentially, you still want this to save, but you are overwriting the original save function,
        #so you need to ref something else.
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

#allows you to change 'metadata' so like 'intrinsic' properties of a Class
    class Meta:
        verbose_name_plural = 'categories'

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    #required to link UserProfile to User
    #when to use OneToOneField vs ForeignKey... FK feels like OneToMany though
    user = models.OneToOneField(User)
    #blank=True means you can leave blank
    website = models.URLField(blank=True)
    #need PIL (pip install pillow)
    #also need bcrypt
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
