from django import forms
from django.forms import  HiddenInput
from blog.models import Course, Comment, Replie, Section


class CourseCreateForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['instructor', 'domainId', 'title', 'image', 'description',
                  'duration', 'price', 'level', 'you_will_learn']


class SectionCreateForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = ['idCours', 'title', 'description', 'media']


class AddComment(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['user', 'idCours', 'comment']

    def __init__(self, *args, **kwargs):
        super(AddComment, self).__init__(*args, **kwargs)
        self.fields['user'].widget = HiddenInput()
        self.fields['idCours'].widget = HiddenInput()


class AddReply(forms.ModelForm):

    class Meta:
        model = Replie
        fields = ['user', 'idComment', 'reply']


