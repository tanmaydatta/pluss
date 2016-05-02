from django.shortcuts import render
import requests
from django.template import Context
from django.http import *
from django.template.loader import get_template
from django.views.decorators.csrf import *
# from auth import *
from models import *
import hashlib
import os
import ipdb
from django.db.models import *
import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



@csrf_exempt
def login(request):
	if request.method == 'GET':
		user_logged_in = request.session.get('logged_in',False)
		if user_logged_in:
			return HttpResponseRedirect('../home')
		return render(request,'index.html')
	elif request.method == 'POST':
		if request.POST.get('username')!= '' and request.POST.get('password')!= '':
			user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if user is not None:
				login_user(request, user)
				return HttpResponseRedirect('../home')
			else:
				return HttpResponseRedirect('../login')
		else :
			return HttpResponseRedirect('../login')
	else:
		response = {
            'status':'failed',
            'error':'not a post or get request'
        }
		return HttpResponse(json.dumps(response))


@login_required
def home(request):
	return render(request,'home.html')

