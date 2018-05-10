from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    difficulty_num = models.IntegerField(default=0)
    simple_num = models.IntegerField(default=0)
    reminding_num = models.IntegerField(default=0)
    understanding_num = models.IntegerField(default=0)
    creativity_num = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = (
        ('D', 'difficult'),
        ('S', 'simple')
    )
    OBJECTIVE_CHOICES = (
        ('R', 'reminding'),
        ('U', 'understanding'),
        ('C', 'creativity')
    )
    content = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    objective = models.CharField(max_length=1, choices=OBJECTIVE_CHOICES)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Choice(models.Model):
    content = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Exam(models.Model):
    pass
