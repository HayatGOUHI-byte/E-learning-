from django.db import models
from django.utils import timezone
from users.models import CustomUser as User
from django.urls import reverse
from .validators import validate_video


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Domain(models.Model):
    domainId = models.CharField(primary_key=True, max_length=15)
    title = models.CharField(max_length=255)
    image = models.ImageField(default='default.jpg', upload_to='domain_images')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('domain-courses', kwargs={'domainId': self.domainId})


class Student(models.Model):
    studentId = models.CharField(primary_key=True, max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=15)
    university = models.CharField(max_length=50)
    linkedIn = models.URLField(blank=True, null=True)
    verified = models.BooleanField(default=False)


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    domainId = models.ForeignKey(Domain, on_delete=models.PROTECT)
    verified = models.BooleanField(default=False)
    company = models.CharField(max_length=100)
    linkedIn = models.URLField(unique=True)
    diploma = models.ImageField(default='default.jpg', upload_to='deploma_pics')


class Course(models.Model):

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    domainId = models.ForeignKey(Domain, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='course_image')
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    creationDate = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    level = models.CharField(max_length=100)
    you_will_learn = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'pk': self.pk})


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    idCours = models.ForeignKey(Course, on_delete=models.PROTECT)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField()
    enroll = models.BooleanField(default=False)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idCours = models.ForeignKey(Course, on_delete=models.CASCADE)
    enumerate = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    Rate = models.CharField(
        max_length=2,
        choices=enumerate,
        null=True,
        blank=True
    )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idCours = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField()


class Replie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idComment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply = models.TextField(default='default reply')


class Section(models.Model):
    idCours = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(default=idCours, max_length=100)
    description = models.TextField()
    media = models.FileField(upload_to="videos", validators=[validate_video])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('section-detail', kwargs={'pk': self.pk})