from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)
    

#--------------------------create team functionality------------------------#

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_team')


    def __str__(self):
        return self.name

class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_member')

    def __str__(self):
        return f"{self.user.username} - {self.team.name}"
    

#---------------task functionality-------------------------------------#

class Task(models.Model):
    
    # Define choices for task priority
    HIGH_PRIORITY = 'high'
    NORMAL_PRIORITY = 'normal'
    LOW_PRIORITY = 'low'

    PRIORITY_CHOICES = [
        (HIGH_PRIORITY, 'High Priority'),
        (NORMAL_PRIORITY, 'Normal Priority'),
        (LOW_PRIORITY, 'Low Priority'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='task_team',null=True,blank=True)
    title = models.CharField(max_length=255)
    description =  models.TextField()
    # Field with choices for priority
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=NORMAL_PRIORITY)
    due_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='task_creator',null=True,blank=True)

    def __str__(self):
        return self.title


class TaskMember(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE,related_name='team_task')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='member_task')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_task')
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.task} - {self.assigned_to}"
    
