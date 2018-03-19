from django.shortcuts import render


def about(request):
	return render(request, 'websiteapp/about.html')

