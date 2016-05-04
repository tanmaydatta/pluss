from django.shortcuts import render
import requests
from django.template import Context
from django.http import *
from django.template.loader import get_template
from django.views.decorators.csrf import *
# from auth import *
from models import *
import json
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

def get_all_data():
	data = {}
	data['salts'] = []
	data['sku_type'] = []
	data['manufacture'] = []
	salts = SaltName.objects.all()
	sku_type = SkuType.objects.all()
	manufacture = ManufactureName.objects.all()
	for i in salts:
		data['salts'].append(i.getDetails())
	for i in sku_type:
		data['sku_type'].append(i.type)
	for i in manufacture:
		data['manufacture'].append(i.name)
	return data


@login_required
#@csrf_exempt
def add(request):
	if request.method == "GET":
		return render(request, 'add.html', get_all_data())
	elif request.method == "POST":
		add_type = request.POST.get('type')
		name = request.POST.get('name')
		if add_type == 'salt':
			obj = SaltName(name=name)
			obj.save()
			log = Logs(msg="New salt added, name = " + name, user=request.user)

		elif add_type == 'manufacture':
			obj = ManufactureName(name=name)
			obj.save()
			log = Logs(msg="New manufacture added, name = " + name, user=request.user)

		elif add_type == 'product':
			try:
				manufacture = request.POST.get('manufacture')
				manufacture = ManufactureName.objects.filter(name=manufacture)[0]
			except:
				response = {
		            'status':'failed',
		            'error':'manufacture name incorrect or not passed'
		        }
				return HttpResponse(json.dumps(response))
			try:
				sku = request.POST.get('sku_type')
				sku = SkuType.objects.filter(name=sku_type)[0]
			except:
				response = {
		            'status':'failed',
		            'error':'sku_type incorrect or not passed'
		        }
				return HttpResponse(json.dumps(response))
			try:
				salts = request.POST.get('salts')
				saltmap = []
				for s in salts:
					saltmap.append((SaltName.objects.filter(name=s['name'])[0],s))

			except:
				response = {
		            'status':'failed',
		            'error':'salt names incorrect or not passed'
		        }
				return HttpResponse(json.dumps(response))
			try:
				pack_size = request.POST.get('pack_size')
			except:
				response = {
		            'status':'failed',
		            'error':'pack_size not passed'
		        }
				return HttpResponse(json.dumps(response))
			try:
				drug_form = request.POST.get('drug_form')
			except:
				response = {
		            'status':'failed',
		            'error':'drug_form not passed'
		        }
				return HttpResponse(json.dumps(response))
			try:
				pack_form = request.POST.get('pack_form')
			except:
				response = {
		            'status':'failed',
		            'error':'pack_form not passed'
		        }
				return HttpResponse(json.dumps(response))
			p_obj = Products(name=name,manufacture=manufacture,pack_size=pack_size,pack_form=pack_form,drug_form=drug_form,sku_type=sku_type)
			p_obj.save()
			for salt in saltmap:
				obj = ProductSaltMap(product=p_obj,salt=salt[0],salt_strength=salt[1]['s_str'],strength_unit=salt[1]['str_unit'])
				obj.save()

			log = Logs(msg="New product added, name = " + name, user=request.user)
				
			response = {
	            'status':'success',
	            'msg':'new product added'
	        }
			return HttpResponse(json.dumps(response))
	else:
		response = {
            'status':'failed',
            'error':'not a post or get request'
        }
		return HttpResponse(json.dumps(response))



def search(request):
	if request.method == "GET":
		response = {}
		query = request.GET['q']
		medicine = Products.objects.filter(name__icontains=query)
		salts = SaltName.objects.filter(name__icontains=query)
		response['products'] = []
		response['salts'] = []
		for i in medicine[:5]:
			response['products'].append(i.getDetails())
		for i in salts[:5]:
			response['salts'].append(i.getDetails())
		response['status'] = 'success'
		return HttpResponse(json.dumps(response))
	else:
		response = {
            'status':'failed',
            'error':'not a get request'
        }
		return HttpResponse(json.dumps(response))

def get_product(request):
	if request.method == "GET":
		response = {}
		id = request.GET['id']
		product = Products.objects.get(id=id)
		saltmap = ProductSaltMap.objects.filter(product=product)
		availability = Availability.objects.filter(product = product)
		response['product'] = product.getDetails()
		response['saltmap'] = []
		response['availability'] = []
		for i in saltmap:
			response['saltmap'].append(i.getDetails())
		for i in availability:
			response['availability'].append(i.getDetails())
		response['status'] = 'success'
		return HttpResponse(json.dumps(response))
	else:
		response = {
            'status':'failed',
            'error':'not a get request'
        }
		return HttpResponse(json.dumps(response))

