# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect, HttpResponse
from django.template import  Context
from django.template.loader import get_template
from db.models import Administrator,Teacher,Student 

def login(request):
    error = []
    logged = False
    submit = False #Ture和False不要加引号！！！！！
    if request.method == 'POST':
        submit = True
        if request.POST.get('user','') and request.POST.get('passwd',''):
            user = request.POST['user']
            passwd = request.POST['passwd']
            if request.POST.get('role','') == 'student':
                try:
                    userint = int(user)#只允许输入数字作为用户名
                except ValueError:
                    error.append("Your username is not in the correct format")
                else:
                    try:
                        r = Student.objects.get(sID = userint)
                        if r.sPasswd == passwd:
                            logged = True
                            request.session['uid'] = r.sID
                            request.session['group'] = 's'
                            request.session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                        else:
                            error.append("Your username and password didn't match.") 
                    except Student.DoesNotExist:
                        error.append("Your username and password didn't match.")
            
            if request.POST.get('role','') == 'administrator':
                try:
                    userint = int(user)
                except ValueError:
                    error.append("Your username is not in the correct format")
                else:
                    try:
                        r = Administrator.objects.get(aID = userint)
                        if r.aPasswd == passwd:
                            logged = True
                            request.session['uid'] = r.aID
                            request.session['group'] = 'a'
                            request.session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                        else:
                            error.append("Your username and password didn't match.") 
                    except Administrator.DoesNotExist:
                        error.append("Your username and password didn't match.") 
            if request.POST.get('role','') == 'teacher':
                try:
                    userint = int(user)
                except ValueError:
                    error.append("Your username is not in the correct format")
                else:
                    try:
                        r = Teacher.objects.get(tID = userint)
                        if r.tPasswd == passwd:
                            logged = True
                            request.session['uid'] = r.tID
                            request.session['group'] = 't'
                            request.session.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
                        else:
                            error.append("Your username and password didn't match.") 
#Fliter找不到列表为空，不抛异常，模型里Get找不到才会抛异常
                    except Teacher.DoesNotExist:
                        error.append("Your username and password didn't match.") 
            if not error:
                return HttpResponseRedirect('/result/')
        else:
            error.append("Username or Password is blank!")

    t = get_template('login.html')
    html = t.render(Context({"errors":error,"submit":submit}))
    return HttpResponse(html)
def result(request):
    return HttpResponse('Managed to Login')
def admin(request):
    return HttpResponse('Admin Page')
def check(request):
    return HttpResponse('Assignment Check Page')
def student(request):
    return HttpResponse('Student main Page')
def submit(request):
    return HttpResponse('Main submit Page')