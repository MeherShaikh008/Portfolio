from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50, help_text="Percentage of proficiency (0-100)")

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True, help_text="Link to a project image")
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50, default="Web App", help_text="e.g. Web App, Data Science, Script")
    technologies = models.CharField(max_length=255, help_text="Comma-separated list of technologies used")

    def __str__(self):
        return self.title

class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current")
    description = models.TextField()

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.role} at {self.company}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class PageVisit(models.Model):
    path = models.CharField(max_length=500)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['path', 'timestamp']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.path} - {self.timestamp}"

    @property
    def page_name(self):
        """Get human-readable page name from path"""
        path_map = {
            '/': 'Home',
            '/experience/': 'Experience',
            '/skills/': 'Skills',
            '/projects/': 'Projects',
            '/contact/': 'Contact',
            '/login/': 'Login',
            '/logout/': 'Logout',
            '/signup/': 'Signup',
            '/admin/': 'Admin Dashboard',
        }
        return path_map.get(self.path, self.path)
