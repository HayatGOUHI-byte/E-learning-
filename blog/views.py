from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
import json
from operator import attrgetter
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from users.models import CustomUser
from .forms import CourseCreateForm, AddComment, SectionCreateForm
from .models import (
    Course,
    Domain, Section, Payment, Comment, Student, Instructor,
)


def landing(request):
    return render(request, "blog/landing-page.html")


"""def domain.css(request):
    context = {
        'domains': Domain.objects.all()
    }
    return render(request, "blog/domain.css.html", context)"""

"""def course(request, domainid):
    context = {
        'courses': Course.objects.filter(domainId=domainid)
    }
    return render(request, "blog/home.html", context)"""


def searchCourses(request):
    context = {}
    if request.method == 'GET':
        search = request.GET['searched']
        queries = search.split(" ")
        queryset = []
        for q in queries:
            courses = Course.objects.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(you_will_learn__icontains=q) |
                Q(level__icontains=q) |
                Q(price__icontains=q)).distinct()

            for course in courses:
                queryset.append(course)
        courses = sorted(list(set(queryset)), key=attrgetter('creationDate'), reverse=True)
        context['searched'] = str(search)
        context['courses'] = courses
    return render(request, 'blog/search_courses.html', context)


class DomainListView(ListView):
    model = Domain
    template_name = 'blog/domain.html'
    context_object_name = 'domains'
    ordering = ['title']
    # paginate_by = 5


class CourseListView(ListView):
    model = Course
    template_name = 'blog/course.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'courses'
    ordering = ['-creationDate']


class InstructorCourseListView(ListView):
    model = Course
    template_name = 'blog/Instructor_courses.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'courses'
    ordering = ['-creationDate']

    def get_queryset(self):
        return Course.objects.filter(instructor=self.request.user.instructor)


class UserCourseListView(ListView):
    model = Payment
    template_name = 'blog/user_courses.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'courses'
    ordering = ['-creationDate']

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class ProfileListView(ListView):
    model = CustomUser
    template_name = 'users/profile.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'user'
    ordering = ['-creationDate']

    def get_queryset(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Payment.objects.filter(user=self.request.user)
        return context


class CourseDetailView(DetailView):
    template_name = 'blog/couse_detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context['sections'] = Section.objects.filter(idCours=course)
        return context


class DomainCourseListView(ListView):
    model = Course
    template_name = 'blog/domain_courses.html'
    context_object_name = 'courses'
    ordering = ['-creationDate']

    # paginate_by = 5
    def get_queryset(self):
        domainid = get_object_or_404(Domain, domainId=self.kwargs.get('domainId'))
        return Course.objects.filter(domainId=domainid).order_by('-creationDate')


class SectionCourseListView(ListView):
    model = Section
    template_name = 'blog/section_course.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'sections'
    paginate_by = 5

    @property
    def get_queryset(self):
        course = get_object_or_404(Course, idCours=self.kwargs.get('idCours'))
        return Section.objects.filter(idCours=course).order_by("title")


class SectionDetailView(DetailView):
    model = Section
    template_name = 'blog/section.html'
    context_object_name = 'section'

    def get_queryset(self):
        section = get_object_or_404(Section, pk=self.kwargs.get('pk'))
        return Section.objects.filter(pk=section.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        section = get_object_or_404(Section, pk=self.kwargs.get('pk'))
        context['object'] = section.idCours
        return context


class CourseEnrolledDetailView(DetailView):
    model = Course
    template_name = 'blog/couse_enrolled_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context['sections'] = Section.objects.filter(idCours=course)
        return context


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = "blog/create_course.html"
    fields = ['instructor', 'domainId', 'title', 'image', 'description', 'duration', 'price', 'level', 'you_will_learn']

    def form_valid(self, form):
        form.instance.user = self.request.user.instructor
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course-detail', kwargs={'pk': self.object.pk})


def createCourse(request):
    if request.method == 'POST':
        form = CourseCreateForm(request.POST,
                                request.FILES)

        form.fields["instructor"].initial = request.user.instructor
        form.fields["instructor"].disabled = True
        if form.is_valid():
            form.save()
            return redirect('created_courses')
    else:
        form = CourseCreateForm(instance=request.user)
        form.fields["instructor"].initial = request.user.instructor
        form.fields["instructor"].disabled = True
    return render(request, 'blog/create_course.html', {'form': form})


def createSection(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = SectionCreateForm(request.POST,
                                request.FILES)

        form.fields["idCours"].initial = course
        form.fields["idCours"].disabled = True
        if form.is_valid():
            form.save()
            return redirect('course-detail', pk=pk)
    else:
        form = SectionCreateForm()
        form.fields["idCours"].initial = course
        form.fields["idCours"].disabled = True
    return render(request, 'blog/create_section.html', {'form': form})


class SectionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Section
    fields = [ 'title', 'description', 'media']
    template_name = 'blog/update_section.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        section = self.get_object()
        if self.request.user == section.idCours.instructor.user:
            return True
        return False


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['title', 'image', 'description', 'duration', 'price', 'level', 'you_will_learn']
    template_name = 'blog/update_course.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.instructor.user:
            return True
        return False


def coursdetail(request, pk):
    course = Course.objects.get(pk=pk)
    comments = Comment.objects.filter(idCours=course)
    sections = Section.objects.filter(idCours=course)
    enroll = Payment.objects.filter(idCours=course, user=request.user)

    if request.method == 'POST':
        form = AddComment(request.POST)
        form.fields["user"].initial = request.user
        form.fields["idCours"].initial = course

        if form.is_valid():
            comm = request.POST['comment']
            form.fields["comment"] = comm
            print(comm)
            form.save()
            return redirect('course-detail', pk=pk)

    else:
        form = AddComment(instance=request.user)
        form.fields["user"].initial = request.user
        form.fields["idCours"].initial = course

    context = {
        "course": course,
        "sections": sections,
        "enroll": enroll,
        "comments": comments,
        "form": form,
    }
    return render(request, 'blog/couse_detail.html', context)


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
    success_url = '/'

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.user:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)
    course = Course.objects.get(id=body['courseId'])
    Payment.objects.create(
        idCours=course,
        user=request.user
    )

    return JsonResponse('Payment completed!', safe=False)


def checkout(request, pk):
    course = Course.objects.get(id=pk)
    context = {'course': course,
               }
    return render(request, 'blog/checkout.html', context)


def dashData(request):
    numcoursres = []
    numenrolls = []
    domains = Domain.objects.all()
    courses = Course.objects.all()
    payments = Payment.objects.all()
    users = CustomUser.objects.all()
    students = Student.objects.all()
    nbs = students.count()
    instructors = Instructor.objects.all()
    nbi = instructors.count()
    nbu = 0
    ids = []
    idi = []
    for id in instructors.values('user'):
        idi.append(id['user'])
    for id in students.values('user'):
        ids.append(id['user'])
    for user in users:
        if user.pk in ids:
            continue
        else:
            if user.pk in idi:
                continue
            else:
                nbu += 1
    nbu = (nbu * 100)/users.count()
    nbs = (nbs * 100) / users.count()
    nbi = (nbi * 100) / users.count()
    userspercentage = [nbu, nbi, nbs]
    datesp = []
    datesc = []
    datesu = []
    # users registeration date
    """for user in users:
        print(user.date_joined)"""
    for m in range(12):
        mounth = CustomUser.objects.filter(date_joined__month=m+1)
        if not mounth:
            datesu.append(0)
        else:
            id = mounth
            listusers = []
            for d in id:
                listusers.append(d.pk)
            datesu.append(len(listusers))
    # payment per mounth
    for m in range(12):
        mounth = Payment.objects.filter(date__month=m+1)
        if not mounth:
            datesp.append(0)
        else:
            id = mounth.values('idCours')
            if id.count() > 1:
                listcourses = []
                prices = []
                for d in id:
                    listcourses.append(d['idCours'])
                    prices.append(float(Course.objects.filter(pk=d['idCours']).values('price')[0]['price']))
                datesp.append(sum(prices))
            else:
                datesp.append(float(Course.objects.filter(pk=id[0]['idCours']).values('price')[0]['price']))
    # courses created per mounth
    for m in range(12):
        mounth = Course.objects.filter(creationDate__month=m+1)
        if not mounth:
            datesc.append(0)
        else:
            id = mounth
            listcourses = []
            for d in id:
                listcourses.append(d.pk)
            datesc.append(len(listcourses))
    # how many courses in domain
    for domain in domains:
        i = 0
        j = 0
        for course in courses:
            for payment in payments:
                if payment.idCours.pk == course.pk:
                    if course.domainId.pk == domain.pk:
                        j += 1
                        break
            if course.domainId.pk == domain.pk:
                i += 1
        numcoursres.append(i)
        numenrolls.append(j)
    context = {
        "domains": domains,
        "numcoursres": numcoursres,
        "numenrolls": numenrolls,
        "payments": payments,
        "datesp": datesp,
        "datesc": datesc,
        "datesu": datesu,
        "userspercentage": userspercentage
    }
    return render(request, 'blog/dashboard.html', context)

