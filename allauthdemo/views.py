from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def member_index(request):
    t = loader.get_template('member/member-index.html')
    c = {}  #{'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='text/html')

@login_required
def member_action(request):
    t = loader.get_template('member/member-action.html')
    c = {}  #{'foo': 'bar'}
    return HttpResponse(t.render(c, request), content_type='text/html')

