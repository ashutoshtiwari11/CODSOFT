from django.shortcuts import render, redirect
from .forms import CourseInfoForm, QuizForm
from .models import Course, Quiz, Progress
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .models import CustomUser
from django.core.mail import EmailMessage #send_mail is another one that can send text data
import json
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User 

def home(request):
    courses=list(Course.objects.all())
    return render(request,'../templates/home.html',{'courses':courses})

def quiz(request,id):
    course = Course.objects.get(id=id)
    quiz_data = Quiz.objects.get(fr_ky= course)
    path = '.'+quiz_data.data.url
    course_id = id
    f = open( path, 'r')
    data = json.load(f)
    return render(request,'../templates/quiz.html', {'data': data, 'id': course_id})

def courses(request):
    courses = list(Course.objects.all())
    return render(request, '../templates/new_courses.html',{'courses': courses})

def course_upload(request):
    if request.method == 'POST':
        form = CourseInfoForm(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          messages.success(request, 'SucessFully Created')
          return redirect('quiz_upload')
        else:
        # Print or log form errors for debugging
              messages.error(request,'Could not Create Course!')
              return redirect('home')  
    else:
        # If it's not a POST request, create an empty form
        form = CourseInfoForm()
        return render(request, '../templates/course_upload.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        # Extract data from the request
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']
        typeofaccount = request.POST['typeofaccount']
        country = request.POST['country']
        city = request.POST['city']

        # Handle image upload
        img = request.FILES.get('img')  # Get the uploaded image
        try:
                user = User.objects.create_user(username=email, password=password)
                custom_user = CustomUser.objects.create(
                     fr_ky=user,  # Set the foreign key to the User instance
                     fname=fname,
                     lname=lname,
                     typeofaccount=typeofaccount,
                     country=country,
                     city=city,
                     img=img)
                # Log the user in
                login(request, user)
                messages.success(request,'Welcome @'+user)
                # Redirect to the home page or another desired page
                return redirect('home')
        except:
                messages.error(request,'User Already Exists!')
        
    return render(request, 'user_register.html',{'content_required': 'register' })

def quiz_upload(request):
     if request.method == 'POST':
        form = QuizForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucefully submited')
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request,'Unexpected Input was Observed')
            return render(request, '../templates/quiz_upload.html',{'form': form}) 
     else:
        form = QuizForm()
        return render(request, '../templates/quiz_upload.html',{'form': form}) 


def user_authentication(request):
    if request.method == 'POST':
        email = request.POST['uname']
        pswd = request.POST['pswd']

        # Check if the user is already authenticated
        if request.user.is_authenticated:
            messages.success(request, f'You are already logged in as {request.user}')
            return redirect('home')
        
        user = authenticate(request, username=email, password=pswd)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user}!')
            return render(request, '../templates/home.html')
        else:
            messages.error(request, 'Sorry, Invalid Details.')
            return redirect('home')
    else:
        content_required = 'login'
        return render(request, '../templates/user_register.html', {'content_required': content_required})


def profile(request):
    user=User.objects.get(username=request.user)
    profile=CustomUser.objects.get(fr_ky=user)
    try:
        enrolled = list(Progress.objects.filter(user=user))
    except:
        enrolled=[]
        
    return render(request,'../templates/profile.html',{'profile': profile,'enrolled': enrolled})

def try_courses(request,id):
    course = Course.objects.get(id=id)
    return render(request,'../templates/try_course.html',{'course':course})
       
def complete_course(request,id):
    ky=id
    user=User.objects.get(username=request.user)
    course=Course.objects.get(id=ky)
    quizz=Quiz.objects.get(fr_ky = course)
    progress, created = Progress.objects.get_or_create(user=user, course=course)
    return render(request,'../templates/complete_course.html',{'course': course,'quizz': quizz})
    
def evaluate(request,id):
    eval_data = request.POST
    ky=id
    course=Course.objects.get(id=ky)
    quiz_data = Quiz.objects.get(fr_ky= course)
    path = '.'+quiz_data.data.url
    f = open(path, 'r')
    data = json.load(f)
    score=0
    eval_counter = 0 
    for i in data['questions']:
        answer = i['answer']
        eval_counter+=1
        choice_counter=0
        for choice_val in i['choices']:
            choice_counter+=1
            if choice_val == answer:
                if str(choice_counter) == eval_data['q'+str(eval_counter)]:
                    score+=1
                else:
                    break
    percent = score / (len(eval_data)-1)*100
    status='Fail'
    if percent  >= 50:
        user=User.objects.get(username=request.user)  
        progress = Progress.objects.get(user=user, course=course)
        progress.completed = True
        progress.save()
        status='Completed'

    return render(request, '../templates/sucessfull.html', {'status': status, 'score': score, 'percent': percent, 'course_id': id})

def certification(request):
    subject="Course Completion Certificate from Course"
    body = "We are glad to have you as a part of our community. Here is Your Ceriffication for the course completion."
    frm = settings.EMAIL_HOST_USER
    to=[request.user]
    email = EmailMessage(subject, body, frm, to)
    image_path = './static/certificate.jpg'
    email.attach_file(image_path)
    email.send()
    messages.success(request, '0hi we have mailed you your email')
    return redirect('home')

def logout(request):
    django_logout(request)
    messages.success(request, 'sucessfully loged out!')
    return redirect('home')


