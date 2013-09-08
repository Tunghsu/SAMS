# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect, HttpResponse
from django.template import  Context
from django.template.loader import get_template
from django.db.models import Count
from db.models import Administrator, Teacher, Student, Student_Class_Relation, Course, Class_Course_Relation, Assignment, AssignmentFile
from django.shortcuts import render_to_response

def login(request):
    error = []
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
    html = t.render(Context({"errors":error,"submit":submit,"title":"学生作业管理系统"}))
    return HttpResponse(html)
def result(request):
    return HttpResponse('Managed to Login')
def admin(request):
    return HttpResponse('Admin Page')
def check(request):
    return HttpResponse('Assignment Check Page')
def view(request):
    return HttpResponse('Teacher main Page')
def submit(request):
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'s'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    #确认只有学生用户才能进行操作
    m = Student_Class_Relation.objects.filter(sID = request.session['uid']).order_by("sClID")
    
    #num = Student_Class_Relation.objects.annotate(number = Count('sClID'))[0].number
    line = {}
    matrix = []
    """
    classNum = []
    courseName = []
    teacher = []
    population = []
    assignmentNum= []
    expire  = []
    assignmentDetail= []
    #if not m:返回一个False值，不显示列表
    #传入二维数组是s
    """
    if not m:
        pass
    else:
        #try:
            for i in m:
                #迭代、序列两种方式可以实现,这里只能用序列
                line['classNum']=i.clID
                cid = Class_Course_Relation.objects.get(clID = i.clID).cID
                line['courseName'] = Course.objects.get(cID = cid).cName
                teacherID = Class_Course_Relation.objects.get(clID = i.clID).tID
                line['teacher'] = Teacher.objects.get(tID = teacherID).tName
                line['population'] = Class_Course_Relation.objects.get(clID = i.clID).cPopu
                line['assignmentNum'] = Assignment.objects.filter(clID = line['classNum']).order_by("-asDate")[0].asID
                line['expire'] = Assignment.objects.get(asID = line['assignmentNum']).asExpire
                tmp = '%d' %line['assignmentNum']#格式化字符串,int -> string
                line['assignmentDetail'] = 'http://localhost:8000/detail/'+tmp
                found =  AssignmentFile.objects.filter(asID = line['assignmentNum'], sID = request.session['uid'])
                if found:
                    line['finish'] = "已提交"
                else:
                    line['finish'] = "尚未提交"
                matrix.append(line)
        #except :
            #数据库出错 
            #print 'Failed' 
            #pass 
            t = get_template('stuhome.html')       
            html = t.render(Context({'matrix':matrix, 'title':"作业提交模块"}))    
            return HttpResponse(html)
    return HttpResponse('Main submit Page')
def viewAssignment(request, offset):
    #try:
        para = int (offset)
    #except:
        #URL错误
        #pass
        txt = Assignment.objects.get(asID = para).asTXT;
        return  render_to_response('blank.html', {'title': "作业详情",'txt':txt})