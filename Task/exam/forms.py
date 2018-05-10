from django import forms

from .models import Question, Course


class QuestionForm(forms.ModelForm):
    Choice1 = forms.CharField(max_length=200)
    Choice2 = forms.CharField(max_length=200)
    Choice3 = forms.CharField(max_length=200)
    correct_answer = forms.IntegerField(min_value=1, max_value=3, label="number Of correct answer")


    class Meta:
        model = Question
        fields = ['content', 'Choice1', 'Choice2', 'Choice3',
                  'correct_answer','difficulty', 'objective', ]


class CouresForm(forms.ModelForm):
    numberOfChapter = forms.IntegerField(min_value=0, label="number Of Chapter")

    class Meta:
        model = Course

        fields = ['name', 'numberOfChapter']
