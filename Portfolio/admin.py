from django.contrib import admin
from .models import Skill, Project, Experience, ContactMessage, PageVisit

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'github_link', 'live_link')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'role', 'start_date', 'end_date')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')

@admin.register(PageVisit)
class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('path', 'user', 'ip_address', 'referrer', 'timestamp')
    readonly_fields = ('path', 'user', 'ip_address', 'referrer', 'user_agent', 'session_key', 'timestamp')
    search_fields = ('path', 'ip_address', 'user__username')
    list_filter = ('path', 'timestamp')
    ordering = ('-timestamp',)
