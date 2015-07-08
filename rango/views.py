#csrf goes in the html template

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#https://docs.djangoproject.com/en/1.7/ref/request-response/#django.http.HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.models import Category, Page


#don't delete this index later.. just comment out
#basically the dictionary has key that can be used as template variable
#so when you have something like post that depends on a pk#,
#your post template variable will change accordingly.
#{{ template_variable }}
#the created dictionary is called the context_dictionary
def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by no. likes in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine
    categories = Category.objects.order_by('-likes')[:5]
    pages = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': categories}
    context_dict['pages'] = pages
    #renders response and sends it back
    return render(request, 'rango/index.html', context_dict)

def about():
    return HttpResponse('ugggg')

def category(request, category_name_slug):
    #remember that the vars you define here will be for the context_dict
    #and will be used as template variables for one reason or other in templates
    #these variables in the templates also hold their respective attr's like var.name
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    context_dict['category_name'] = category.name

    pages = Page.objects.filter(category=category)
    context_dict['pages'] = pages
    context_dict['category_name_slug'] = category_name_slug
    context_dict['category'] = category
    return render(request, 'rango/category.html', context_dict)

#this view function can do 3 things:
#1) show blank form
#2) save data associated with model -> go to index
#3) show errors
def add_category(request):
    #don't forget to make POST a string
    #i think... this makes it so you either get the empty form (else) or you do the (if) and post it which...
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        #if the form is filled out correctly, you save and commit it
        #remember the form (CategoryForm) is linked to Category model and save will act as you expect
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        #otherwise you print errors
        else:
            print(form.errors)
    else:
        #i think tutorial says this is a 'GET', which kinda makes sense because you're getting data
        #i think django does something to change it to post (although you do explicitly say it too up there)
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form })

#review the logic here... and how it connects to category
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    #so basically... going to the url you get the (else) which is GET the form
    #when you hit submit you POST which carries out the (if)
    #don't forget to string POST
    if request.method == 'POST':
        form = PageForm(request.POST)
        #so check if everything is filled out or else print errors
        if form.is_valid():
            if cat:
                #not sure what commit does
                #remember that PageForm has title & url fields
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                #save category and views
                page.save()
                #go back to category view
                return category(request, category_name_slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    #initial registered is False... gets set to True after registering
    registered = False
    #i think this is how you show 2 forms? feel like there would be 2 submit buttons?
    #actually no i think submit depends on the html and you can just combine both
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and user_profile_form.is_valid():
            user = user_form.save()
            #hash the password and update
            user.set_password(user.password)
            user.save()

            #still need to assign a user to profile, use commit=False to delay saving
            #i think this sets profile be filled out but not 'saved'?
            profile =  user_profile_form.save(commit=False)
            #establish link between profile and user(hidden in profile)
            profile.user = user

            #if prof pic was provided, get from input and put it in UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors)
            print(user_profile_form.errors)
    else:
        user_form = UserForm()
        user_profile_form = UserProfileForm()
                                            #careful not to miss all (template) vars you make
    return render(request, 'rango/register.html', {'user_form': user_form,
                                                   'user_profile_form': user_profile_form,
                                                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        #get user and pass from login form
        #use request.POST.get('<var>') instead of request.POST('<var>') b/c the latter will raise
        #an exception if var is empty, whereas the former will return None
        username = request.POST.get('username')
        password = request.POST.get('password')
        #User object is returned if matches
        user = authenticate(username=username, password=password)
        if user:
            #check if active -- make sure to not use () b/c it's not a method
            #it is a field of user, not a method... will get 'bool' object is not callable error
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('')
            else:
                return HttpResponse('Your account is disabled!')
        else:
            return HttpResponse('Invalid login credentials!')
    #display login form when not submitting -- HTTP GET instead of POST
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')