from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
        return self.name

class Topic(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Lesson(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    document=models.ImageField(upload_to="lesson_Doc/")
    video= models.FileField(upload_to='lesson_videos/') 
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
