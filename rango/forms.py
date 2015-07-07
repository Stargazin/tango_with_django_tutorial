#https://docs.djangoproject.com/en/1.8/ref/forms/widgets/
#https://docs.djangoproject.com/en/1.8/ref/forms/
#a ModelForm is a helper class that allows you to create
#a Django form using a pre-existing model
#1.7+ Meta is required with atleast model= and fields= (or exclude)

from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter a category name.")
    #error_messages=;; make sure this attr is a dictionary otherwise you raise an error
    #dictionary update sequence element #0 has length 1; 2 is required
    #also try to read and understand errors pls lol..
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        #link the ModelForm and model
        model = Category
        #having something in 'field' means it's required... not sure about "not in exclude"
        #but essentially, users can't not fill out a field or else they get an error
        fields = ('name', )

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    #still need to include hidden fields b/c there won't be a 'field' for it otherwise.
    #i think it will still have the attr and resulting values (as specified), but you won't be able to see...?
        #^jk the form wouldn't have the value and you would probably get an error (tutorial says)
        #this is b/c we have initial=0... if you use default=0 instead it should be ok.
        #if you can't use numbers, see 'slug' in 'CategoryForm), you can use required=False
    #also note that above, for CategoryForm->views/likes/slug, we don't list them in the fields
    #probably cause we don't want to show them.
    class Meta:
        model = Page
        #can either specify fields to show (with fields=) or exclude with (exclude=)
        #here we exclude the ForeignKey(Category)
        #so fields=title, url, views
        exclude = ('category', )

    #ultimately, this 'cleans' the data before it gets stored (saved)
    def clean(self):
        #cleaned_data is a dictionary attr (of ModelForm)
        cleaned_data = self.cleaned_data
        #so here you are 'get'ting data from that dictionary^
        #so below (if), if url was not empty, you would get an error b/c nothing would be in the dict
        url = cleaned_data.get('url')
        #if url is not empty and doesn't start with 'http://', add it
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        #so basically, for each field, you can 1) check a value was receieved and then 2) check the value
        #and change it using some logic before 3) reassigning the value back to the cleaned_data dict
        #always end by returning cleaned_data
        return cleaned_data

class UserForm(forms.ModelForm):
    #makes it so password is hidden when being typed
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
