# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect, HttpResponse
from django.template import  Context
from django.template.loader import get_template
from django.db.models import Count
from db.models import Administrator, Teacher, Student, Student_Class_Relation, Course, Class_Course_Relation, Assignment, AssignmentFile
from django.shortcuts import render_to_response
from django.core.servers.basehttp import FileWrapper
import os, mimetypes
import settings

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
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'t'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    m = Class_Course_Relation.objects.filter(tID = request.session['uid']).order_by("clID")
    if not m:
        #无课程
        pass
    else:
        line = {}
        matrix = []
        #try
        for i in m:
            line['classNum'] = i.clID
            line['courseID'] = Class_Course_Relation.objects.get(clID = i.clID).cID
            line['courseName'] = Course.objects.get(cID = line['courseID']).cName
            line['population'] = Class_Course_Relation.objects.get(clID = i.clID).cPopu
            line['assignmentNum'] = Assignment.objects.filter(clID = line['classNum']).order_by("-asDate")[0].asID
            line['finishPopu'] = Assignment.objects.get(asID = line['assignmentNum']).asFinishPopu
            line['assignmentAmount'] = Assignment.objects.filter(clID = i.clID).annotate(number = Count('clID'))[0].number
            tmp = '%d' % line['assignmentNum']#格式化字符串,int -> string
            line['assignmentDetail'] = 'http://localhost:8000/detail/'+tmp
            line['viewassignment'] = 'http://localhost:8000/checkassign/'+tmp
            matrix.append(line)
        t = get_template("teacher.html")
        html = t.render(Context({'title':'教师作业批改系统','matrix':matrix}))
    return HttpResponse(html)
def checkassign(request, offset):
#教师检查作业
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'t'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    try:
        assignmentNum = int (offset)
    except:
        #URL错误
        pass
    classNum = Assignment.objects.get(asID = assignmentNum).clID
    title = '%d' % classNum
    assignstr = '%d' % assignmentNum
    title = title + '班级第'+ assignstr +'次作业统计'
    fileList = AssignmentFile.objects.filter(asID = assignmentNum).order_by("sID")
    line = {}
    matrix = []
    for i in fileList:
        line['studentID'] = i.sID
        line['submitDate'] = i.asfDate
        line['studentName'] = Student.objects.get(sID = i.sID).sName
        assignmentFileNum = '%d' % i.asfID
        line['downloadLink'] = 'http://localhost:8000/download/'+ assignmentFileNum
        matrix.append(line)
    return render_to_response('checkassign.html', {'title': title, 'matrix':matrix})
def submit(request):
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'s'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    #确认只有学生用户才能进行操作
    hint = ''
    if request.method == 'POST':
        #asf自更新加一
        asfID = AssignmentFile.objects.order_by('asfID')[0].asfID+1
        asID = request.POST['radio']
        sID = request.session['uid']
        asfIDStr = '%d' % asfID
        sIDStr = '%d' % sID
        sName = Student.objects.get(sID = sID).sName
        request.FILES['File'].name = sIDStr+'_'+sName+'_'+request.FILES['File'].name
        instance = AssignmentFile(asfID = asfID ,sID = sID, asID = asID, asFile = request.FILES['File'])
        instance.save()
        hint = "Upload succeed"
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
        #无课程
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
            html = t.render(Context({'matrix':matrix, 'title':"作业提交模块", 'hint':hint}))    
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
def download(request, offset):
    #try:
        para = int (offset)
    #except:
        #404
        pass
        #try:
        filefield = AssignmentFile.objects.get(asfID = para).asFile
        files = file(u'/home/tunghsu/workspace/SAMS/media/'+filefield.name)
        wrapper = FileWrapper(files)#分段处理，每段8K
        mimetype = mimetypes.guess_type(u'http://www.aol.com/'+filefield.name)[0]
        print filefield.name
        print mimetype
        response = HttpResponse(wrapper, content_type=mimetype)
        if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
            filename_header = 'filename=%s' % filefield.name.encode('utf-8')
        elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
            filename_header = 'filename=%s' % filefield.name.encode('utf-8')
        #else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        #filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(filefield.name.encode('utf-8'))
        #response = HttpResponse(filefield.read(),mimetype = "image/png")
        response['Content-Length'] = os.path.getsize(u'/home/tunghsu/workspace/SAMS/media/'+filefield.name)
        response['Content-Disposition'] = 'attachment; ' + filename_header#用户名带有路径，需要改
        #response['title'] = filefield.name
        #size = '%d' % file.size()
        #response['Content-Length'] = size
        #except DoesNot Exist
        #Raise 404
        return response
        