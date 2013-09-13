# -*- coding: utf-8 -*- 
from django.http import HttpResponseRedirect, HttpResponse
from django.template import  Context
from django.template.loader import get_template
from django.db.models import Count
from db.models import Administrator, Teacher, Student, Student_Class_Relation, Course, Class_Course_Relation, Assignment, AssignmentFile
from django.shortcuts import render_to_response
from django.core.servers.basehttp import FileWrapper
import os, mimetypes

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
                            if not 'box' in request.POST:
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
                            if not 'box' in request.POST:
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
                            if not 'box' in request.POST:
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
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'a'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    hint = ''
    if 'box' in request.GET:
        for j in request.GET['box']:
            classID = Class_Course_Relation.objects.filter(cID = j).clID
            for i in classID:
                Assignment.objects.filter(clID = i).delete()
                AssignmentFile.objects.filter(clID = i).delete()
                Student_Class_Relation.objects.filter(clID = i).delete()
                Class_Course_Relation.objects.filter(cID = j).delete()
                Course.objects.filter(cID = j).delete()
        hint = 'Course Deleted'
    if 'q' in request.POST:#需要后台检测字符转换数字
        if request.POST['q'] == 'student':
            instance = Student(sID=request.POST['uid'], sName=request.POST['name'],sPasswd=request.POST['passwd'],sMail=request.POST['mail'])
            instance.save()
            hint = 'Add Student Done!'
        elif request.POST['q'] == 'teacher':
            instance = Teacher(tID=request.POST['uid'], tName=request.POST['name'],tPasswd=request.POST['passwd'],tMail=request.POST['mail'])
            instance.save()
            hint = 'Add Teacher Done!'
        elif request.POST['q'] == 'admin':
            instance = Administrator(aID=request.POST['uid'], aName=request.POST['name'],aPasswd=request.POST['passwd'],aMail=request.POST['mail'])
            instance.save()
            hint = 'Add Admin Done!'
    if 'id' in request.POST:
        para =  int (request.POST['id'])
        instance = Course(cID=para, cName=request.POST['name'])
        instance.save()
        hint = 'Add Course Done!'
    if 'amount' in request.POST:
        instance = Class_Course_Relation(cID=request.POST['courseID'], clID=request.POST['classID'],tID=request.POST['teacher'],cPopu=request.POST['amount'])
        instance.save()
        hint = 'Add class Done!'
    if  'className' in request.POST:
        num = Student.objects.filter(sID = request.POST['uid']).order_by('sClID')[0]
        instance = Student_Class_Relation(sID=request.POST['uid'], clID=request.POST['className'],sClID=num)
        instance.save()
        hint = 'Add Student to Class Done!'
    m = Course.objects.all().order_by("cID")
    line ={}
    matrix = []
    for i in m:
        line['courseName'] = i.cName
        line['courseID'] = i.cID
        tmp ='%d' % i.cID
        line['viewcourse'] = 'http://localhost:8000/course/'+tmp
        matrix.append(dict(line))    
    return  render_to_response('admin.html', {'title': "管理页面",  'hint':hint, 'matrix':matrix})
def course(request, offset):
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'a'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    hint = ''
    if 'box' in request.GET:
        for j in request.GET['box']:
            Assignment.objects.filter(clID = j).delete()
            AssignmentFile.objects.filter(clID = j).delete()
            Student_Class_Relation.objects.filter(clID = j).delete()
            Class_Course_Relation.objects.filter(clID = j).delete()
        hint = 'Class Deleted'
    #try:
    para = int (offset)
    #except:
        #URL错误
        #pass
    m = Class_Course_Relation.objects.filter(cID = para).order_by("clID")
    courseStr = Course.objects.get(cID = para).cName
    line = {}
    matrix = []
    for i in m:
        line['classID'] = i.clID
        line['teacher'] = Teacher.objects.get(tID = i.tID).tName
        tmp ='%d' % i.clID
        line['viewcourse'] = 'http://localhost:8000/class/'+tmp
        matrix.append(dict(line))
    return  render_to_response('course.html', {'title': courseStr+"课程班级查看页面", 'matrix':matrix, 'hint':hint})
def classes(request, offset):
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'a'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    hint = ''
    if 'box' in request.GET:
        for j in request.GET['box']:
            AssignmentFile.objects.filter(sID = j).delete()
            Student_Class_Relation.objects.filter(sID = j).delete()
        hint = 'Student of the class Deleted'
    #try:
    para = int (offset)
    #except:
        #URL错误
        #pass
    m = Student_Class_Relation.objects.filter(clID = para).order_by("sID")
    line = {}
    matrix = []
    for i in m:
        line['studentName'] = Student.objects.get(sID = i.sID).sName
        line['studentID'] = i.sID
        matrix.append(dict(line))
    return  render_to_response('class.html', {'title': offset+"班级学生查看页面", 'matrix':matrix,'hint':hint})
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
            matrix.append(dict(line))
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
        matrix.append(dict(line))
    return render_to_response('checkassign.html', {'title': title, 'matrix':matrix})
def submit(request):
    try:
        if (not 'uid' in request.session) or (request.session['group']<>'s'):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    hint = ''
    if request.method == 'POST':
        #asf自更新加一
        asfID = AssignmentFile.objects.order_by('asfID')[0].asfID+1
        asID = request.POST['radio']
        sID = request.session['uid']
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
                try:
                    line['assignmentNum'] = Assignment.objects.filter(clID = line['classNum']).annotate(number = Count('clID'))[0].number
                    if  line['assignmentNum']:
                        print line['assignmentNum']
                        line['assignmentNum'] = Assignment.objects.filter(clID = line['classNum']).order_by("-asDate")[0].asID
                                                #有问题
                        line['expire'] = Assignment.objects.get(asID = line['assignmentNum']).asExpire
                        tmp = '%d' %line['assignmentNum']#格式化字符串,int -> string
                        line['assignmentDetail'] = 'http://localhost:8000/detail/'+tmp
                        found =  AssignmentFile.objects.filter(asID = line['assignmentNum'], sID = request.session['uid'])
                        if found:
                            line['finish'] = "已提交"
                        else:
                            line['finish'] = "尚未提交"
                except:
                    pass
                matrix.append(dict(line))
            #except :
                        #数据库出错 
            #print 'Failed' 
            #pass 
    t = get_template('stuhome.html')       
    html = t.render(Context({'matrix':matrix, 'title':"作业提交模块", 'hint':hint}))    
    return HttpResponse(html)
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
    #try:
    filefield = AssignmentFile.objects.get(asfID = para).asFile
    files = file(u'/home/tunghsu/workspace/SAMS/media/'+filefield.name)
    wrapper = FileWrapper(files)#分段处理，每段8K
    mimetype = mimetypes.guess_type(u'http://www.aol.com/'+filefield.name)[0]
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
def profile(request):
    try:
        if (not 'uid' in request.session) or (request.session['group']==''):
            return HttpResponseRedirect('/login/')
    except KeyError:
        return HttpResponseRedirect('/login/')
    hint=[]
    if request.method == 'POST':
        if request.session['group']=='s':
            if Student.objects.get(sID = request.session['uid']).sPasswd==request.POST['oldpasswd']:
                if request.POST['user']:
                    Student.objects.filter(sID = request.session['uid']).update(sName = request.POST['user'])
                    hint.append("Username Changed")
                if request.POST['mail']:
                    Student.objects.filter(sID = request.session['uid']).update(sMail = request.POST['mail'])
                    hint.append("Email Changed")
                try:
                    if request.POST['passwd']==request.POST['passwd2'] and request.POST['passwd']:
                        Student.objects.filter(sID = request.session['uid']).update(sPasswd = request.POST['passwd'])
                        hint.append('Password Changed')
                except:
                    pass
        if request.session['group']=='t':
            if Teacher.objects.get(tID = request.session['uid']).tPasswd==request.POST['oldpasswd']:
                if request.POST['user']:
                    Teacher.objects.filter(tID = request.session['uid']).update(tName = request.POST['user'])
                    hint.append("Username Changed")
                if request.POST['mail']:
                    Teacher.objects.filter(tID = request.session['uid']).update(tMail = request.POST['mail'])
                    hint.append("Email Changed")
                try:
                    if request.POST['passwd']==request.POST['passwd2'] and request.POST['passwd']:
                        Teacher.objects.filter(tID = request.session['uid']).update(tPasswd = request.POST['passwd'])
                        hint.append("用户密码已更改")
                except:
                    pass
        if request.session['group']=='a':
            if Administrator.objects.get(aID = request.session['uid']).aPasswd==request.POST['oldpasswd']:
                if request.POST['user']:
                    Administrator.objects.filter(aID = request.session['uid']).update(aName = request.POST['user'])
                    hint.append(u"Username Changed")
                if request.POST['mail']:
                    Administrator.objects.filter(aID = request.session['uid']).update(aMail = request.POST['mail'])
                    hint.append("Email Changed")
                try:
                    if request.POST['passwd']==request.POST['passwd2'] and request.POST['passwd']:
                        Administrator.objects.filter(aID = request.session['uid']).update(aPasswd = request.POST['passwd'])
                        hint.append("用户密码已更改")
                except:
                    pass
    return render_to_response('profile.html', {'title': "修改个人信息", 'hint':hint})
def logout(request):
    try:
        if request.session['uid']:
            del request.session['uid']
            del request.session['group']
    except:
        pass
    return HttpResponseRedirect('/login/') 
        