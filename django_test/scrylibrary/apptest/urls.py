from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from apptest.models import Article


urlpatterns = [
	url(r'^$', ListView.as_view(queryset=Article.objects.all().order_by("-date")[:100], template_name="apptest/jinjatest.html"))
]
