from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from websiteapp.models import Article
from . import views


urlpatterns = [
	url(r'^$', ListView.as_view(queryset=Article.objects.all().order_by("-date"), template_name="websiteapp/articles_table.html"), name = 'home'),
	url(r'^about/', views.about, name='about'),
]
