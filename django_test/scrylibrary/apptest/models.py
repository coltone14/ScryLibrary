from django.db import models

class Article(models.Model):
    title = models.CharField(primary_key=True, max_length=150)
    author = models.CharField(primary_key=True, max_length=55)
    date = models.DateField()
    link = models.CharField(unique=True, max_length=255)
    source = models.CharField(max_length=45)
    source_url = models.CharField(unique=True, max_length=60)
    game = models.CharField(max_length=45)
    content_type = models.CharField(max_length=45)
    premium = models.CharField(max_length=1)    #binary

    def __str__(self):
    	return self.title

    class Meta:
        managed = False
        db_table = 'article'

