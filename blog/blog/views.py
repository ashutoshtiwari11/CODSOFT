from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from .models import CustomUser, Post, Comment
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout as django_logout
from .forms import BlogForm
import re

def home(request):
    query = request.GET.get('q')  # Get the search query from the request
    if query:
        # Perform a case-insensitive search in the titles of all Post objects
        posts = Post.objects.filter(title__iregex=r'.*%s.*' % re.escape(query))
    else:
        posts = list(Post.objects.all())
    return render(request, '../templates/allpost.html',{'posts': posts, 'query': query})

def register(request):
    if request.method == 'POST':
        # Extract data from the request
        uname=request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        bio= request.POST['bio']
        phone=request.POST['phone']
        lname = request.POST['lname']
        country = request.POST['country']
        city = request.POST['city']
        img = request.FILES.get('img')  # Get the uploaded image
        try:
               user = User.objects.create_user(username=uname,email=email,first_name=fname,last_name=lname, password=password)
               custom_user = CustomUser.objects.create(
                    fr_ky=user, 
                    Bio=bio,
                    phone=phone,
                    country=country,
                    city=city,
                    img=img      )
               login(request, user)
               messages.success(request,'Welcome @'+user.username)
               return redirect('home')
        except:
            messages.error(request,'Sorry User already Exists.')
    return render(request, 'user_register.html',{'content_required': 'register'})


def authenticated(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        pswd = request.POST['pswd']
        if request.user.is_authenticated:
            messages.success(request, f'You are already logged in as {request.user}')
            return redirect('home')
        user = authenticate(request=request, username=uname , password=pswd)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user}!')
            return redirect('home')
        else:
            messages.error(request, 'Sorry, Invalid Details.')
            return redirect('home')
    else:
        return render(request, '../templates/user_register.html')


def profile(request):
    user=User.objects.get(username=request.user)
    profile=CustomUser.objects.get(fr_ky=user.id)
    try:
        posts = list(Post.objects.filter(user=user))
    except:
        posts = []
        
    return render(request,'../templates/profile.html',{'profile': profile,'post': posts})

def allpost(request):
    posts = list(Post.objects.all())
    return render(request, '../templates/allpost.html',{'posts': posts})

def thepost(request,id):
    if request.user.is_authenticated:
         user=User.objects.get(username=request.user)
         post=Post.objects.get(post_id=id)
         img=CustomUser.objects.get(fr_ky=post.user.id).img.url
         comments=Comment.objects.filter(post=post)
         print(comments)
         return render(request,'../templates/thepost.html',{'post': post,'user': user, 'comments':comments, 'img':img})
    post=Post.objects.get(post_id=id)
    comments=Comment.objects.filter(post=post)
    img=CustomUser.objects.get(fr_ky=post.user.id).img.url
    return render(request,'../templates/thepost.html',{'post': post, 'comments':comments,'img': img})

def comment(request, id):
   if request.method == 'POST':
          comment = request.POST['comment']
          user=User.objects.get(username=request.user)
          post=Post.objects.get(post_id=id)
          slug=request.user
          comments=Comment.objects.create(user= user, post=post, content=comment, slug=slug)
      
          return redirect('home')
   else:
        return redirect('/')

def post(request):
    if request.method == 'POST':
        title=request.POST['title']
        content=request.POST['content']
        pub_date=request.POST['pub_date']
        thumbnail=request.FILES.get('thumbnail')
        print(request.user)
        user=User.objects.get(username=request.user.username)
        blog= Post.objects.create(user=user,title=title,content=content,thumbnail=thumbnail,pub_date=pub_date)
        blog.save()
        messages.success(request,'sucefull uloaded the post!')
        return redirect('home')
    return render(request, 'createblog.html')

def logout(request):
    django_logout(request)
    messages.success(request, 'sucessfully loged out!')
    return redirect('home')






