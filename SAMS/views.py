from django.http import HttpResponse
from django.template import  Context
from django.template.loader import get_template

def login(request):
    error = []
    submit = False #Ture和False不要加引号！！！！！
    if request.method == 'POST':
        submit = 'true'
        if request.POST.get('user',''):
            user = request.POST.get('user','')
        else:
            error.append("Username is invalid!")
        if  request.POST.get('passwd',''):
            passwd = request.POST.get('passwd','')
        else:
            error.append("Password is wrong!")
    t = get_template('login.html')
    html = t.render(Context({"errors":error,"submit":submit}))
    return HttpResponse(html)
def result(request):
    return HttpResponse('Managed to Login')