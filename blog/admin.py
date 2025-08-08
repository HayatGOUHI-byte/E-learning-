from django.contrib import admin
from .models import Domain, Course, Replie, Comment, Section, Student, Instructor, Post, Payment

admin.site.register(Post)
admin.site.register(Payment)
admin.site.register(Instructor)
admin.site.register(Domain)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Replie)
admin.site.register(Comment)
admin.site.register(Section)
