from django.shortcuts import render
from django.http import HttpResponse as hres

def index(request):
	return hres("<h3> DBTest </h3>")
