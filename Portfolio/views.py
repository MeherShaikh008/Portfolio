from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth import authenticate
from datetime import timedelta
from .models import Skill, Project, Experience, ContactMessage, PageVisit
from .forms import EmailUserCreationForm, EmailAuthenticationForm

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def experience(request):
    experiences = Experience.objects.all()
    return render(request, 'experience.html', {'experiences': experiences})

@login_required(login_url='login')
def skills(request):
    skills = Skill.objects.all()
    return render(request, 'skills.html', {'skills': skills})

@login_required(login_url='login')
def projects(request):
    projects = Project.objects.all()
    categories = []

    for project in projects:
        project.tech_list = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
        if project.category not in categories:
            categories.append(project.category)

    return render(request, 'projects.html', {
        'projects': projects,
        'categories': categories
    })

@login_required(login_url='login')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'contact.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = EmailUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
    else:
        form = EmailAuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def dashboard(request):
    user_visits = PageVisit.objects.filter(user=request.user)
    total_visits = user_visits.count()
    recent_visits = user_visits.order_by('-timestamp')[:10]
    last_visit = user_visits.order_by('-timestamp').first()

    context = {
        'total_visits': total_visits,
        'recent_visits': recent_visits,
        'last_visit': last_visit,
    }
    return render(request, 'dashboard.html', context)


def custom_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


@login_required(login_url='login')
def admin_dashboard(request):
    now = timezone.now()
    last_30_days = now - timedelta(days=30)
    last_7_days = now - timedelta(days=7)

    is_admin = request.user.is_staff or request.user.is_superuser

    if not is_admin:
        messages.error(request, 'Admin analytics are available only to staff users.')
        return redirect('dashboard')

    # Get analytics data

    # Total visits
    total_visits = PageVisit.objects.count()

    # Visits in last 30 days
    visits_30_days = PageVisit.objects.filter(timestamp__gte=last_30_days).count()

    # Visits in last 7 days
    visits_7_days = PageVisit.objects.filter(timestamp__gte=last_7_days).count()

    # Unique visitors (by IP)
    unique_visitors = PageVisit.objects.values('ip_address').distinct().count()

    # Page popularity
    page_popularity_qs = PageVisit.objects.values('path').annotate(
        visits=Count('id')
    ).order_by('-visits')[:10]

    max_visits = page_popularity_qs[0]['visits'] if page_popularity_qs else 1
    page_popularity = [
        {
            'path': item['path'],
            'visits': item['visits'],
            'percent': int(item['visits'] / max_visits * 100) if max_visits else 0,
        }
        for item in page_popularity_qs
    ]

    # Daily visits for chart
    daily_visits = PageVisit.objects.filter(timestamp__gte=last_30_days).extra(
        select={'day': 'date(timestamp)'}
    ).values('day').annotate(visits=Count('id')).order_by('day')

    # Recent visits
    recent_visits = PageVisit.objects.select_related('user').order_by('-timestamp')[:20]

    # Contact messages
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(created_at__gte=last_7_days).count()

    context = {
        'total_visits': total_visits,
        'visits_30_days': visits_30_days,
        'visits_7_days': visits_7_days,
        'unique_visitors': unique_visitors,
        'page_popularity': page_popularity,
        'daily_visits': list(daily_visits),
        'recent_visits': recent_visits,
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'is_admin': is_admin,
    }

    return render(request, 'admin_dashboard.html', context)

