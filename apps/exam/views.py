from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def index(request):
    return render(request,'exam/index.html')

def regis(request):
    result = User.manager.regis_validator(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/main')
    
    request.session['user_id'] = result.id
    # messages.error(request, "Successfully registered!")
    return redirect('/friends')

def login(request):
    result = User.manager.login_validator(request.POST)
    if not result:
        messages.error(request, "login info invalid")
        return redirect('/main')
    else:
        request.session['user_id'] = result.id
        # messages.error(request, "Successfully logged in!")
        return redirect('/friends')
    
def logout(request):
    request.session.clear()
    return redirect('/main')

def friends(request):
    try:
        user = User.manager.filter(id=request.session['user_id']),
        context = {
            'user': user[0], 
            'allusers': User.manager.exclude(id=request.session['user_id']),
            'buddy': User.manager.get(id=request.session['user_id']).friends.all()
        }
        return render(request,'exam/result.html',context)

    except KeyError:
        return redirect('/main')

def showuser(request,user_id):
    showuser = User.manager.get(id=user_id)

    context = {
        'showuser': showuser,
        
    }
    return render(request,'exam/user.html',context)

def add(request):
    if request.method:
        User.manager.add_friend(request.POST["friend_id"], request.POST["user_id"])
        return redirect('/friends')