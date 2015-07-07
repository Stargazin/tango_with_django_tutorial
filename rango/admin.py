#customizing admin page
#remember to register all models
#https://docs.djangoproject.com/en/1.8/ref/contrib/admin/

from django.contrib import admin
from models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
