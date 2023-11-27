from .models import Team, TaskMember, Task
from .forms import TeamForm, TaskForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from tasks.models import User
from .forms import TeamForm
from .models import Team
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm
from tasks.helpers import login_prohibited
from django import forms  # Import the forms module
from django.db.models import Case, When
from django.db import models


@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    current_user = request.user
    return render(request, 'dashboard.html', {'user': current_user})


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get(
            'next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR,
                             "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(
            self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(
            self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


# -----------------------create team functionality----------------------------#

# views.py


# @login_required
# def team_list(request):
#     teams = Team.objects.all()
#     return render(request, 'team_list.html', {'teams': teams})

# # @login_required
# def create_team(request):
#     if request.method == 'POST':
#         form = TeamForm(request.POST)
#         if form.is_valid():
#             team = form.save()
#             TeamMember.objects.create(team=team, user=request.user)
#             members = form.cleaned_data.get('members', [])
#             for member in members:
#                 TeamMember.objects.create(team=team, user=member)
#             return redirect('team_list')
#     else:
#         form = TeamForm()
#     return render(request, 'create_team.html', {'form': form})

# # @login_required
# def edit_team(request, team_id):
#     team = get_object_or_404(Team, id=team_id)
#     if request.method == 'POST':
#         form = TeamForm(request.POST, instance=team)
#         if form.is_valid():
#             form.save()
#             # Update team members
#             members = form.cleaned_data.get('members', [])
#             team.members.set(members)
#             return redirect('team_list')
#     else:
#         form = TeamForm(instance=team)
#     return render(request, 'edit_team.html', {'form': form, 'team': team})

# # @login_required
# def delete_team(request, team_id):
#     team = get_object_or_404(Team, id=team_id)
#     if request.method == 'POST':
#         team.delete()
#         return redirect('team_list')
#     return render(request, 'delete_team.html', {'team': team})

# # @login_required
# def remove_teammember(request, team_id, member_id):
#     team = get_object_or_404(Team, id=team_id)
#     member = get_object_or_404(User, id=member_id)
#     if request.method == 'POST':
#         TeamMember.objects.filter(team=team, user=member).delete()
#         return redirect('edit_team', team_id=team_id)
#     return render(request, 'remove_teammember.html', {'team': team, 'member': member})


# class TeamListView(ListView):
#     model = Team
#     template_name = 'team_list.html'
#     context_object_name = 'teams'

#     def get_queryset(self):
#         # Get teams where the logged-in user is a member
#         return Team.objects.filter(members__user=self.request.user)


# class TeamCreateView(CreateView):
#     model = Team
#     form_class = TeamForm
#     template_name = 'team_create.html'
#     success_url = reverse_lazy('team_list')

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         team = form.save()
#         TeamMember.objects.create(team=team, user=self.request.user)
#         members = form.cleaned_data.get('members', [])
#         for member in members:
#             TeamMember.objects.create(team=team, user=member)
#         return super().form_valid(form)

class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'team_create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # team = form.save()
        return super().form_valid(form)

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class)

    #     # Exclude the logged-in user from the members queryset during team creation
    #     form.fields['members'].queryset = User.objects.exclude(
    #         pk=self.request.user.pk)
    #     return form


# class TeamUpdateView(UpdateView):
#     model = Team
#     form_class = TeamForm
#     template_name = 'edit_team.html'
#     success_url = reverse_lazy('team_list')

#     def form_valid(self, form):
#         team = form.save()
#         members = form.cleaned_data.get('members', [])
#         team.members.set(members)
#         return super().form_valid(form)
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'edit_team.html'
    success_url = reverse_lazy('team_list')

    def form_valid(self, form):
        team = form.save(commit=False)
        # members = form.cleaned_data.get('members', [])

        # # Add new members to the team
        # for member in members:
        #     team_member, created = TeamMember.objects.get_or_create(
        #         team=team, user=member)
            # Optionally, you can set additional attributes for the TeamMember here

        team.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        team = self.get_object()
        initial['members'] = team.members.all()
        return initial


class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'delete_team.html'
    success_url = reverse_lazy('team_list')


# ----------------------------task functionality---------------------#

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Get teams where the logged-in user is a member
        # return Task.objects.filter(member_task__assigned_to=self.request.user)
        tasks = Task.objects.filter(created_by=self.request.user).order_by(
            Case(
                When(priority=Task.HIGH_PRIORITY, then=0),
                When(priority=Task.LOW_PRIORITY, then=2),
                When(priority=Task.NORMAL_PRIORITY, then=1),
                default=3,  # Add a default value to handle any other priorities
                output_field=models.IntegerField(),
            )
        )
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['list_type'] = 'creater'
        return context


# class TaskCreateView(CreateView):
#     model = Task
#     form_class = TaskForm
#     template_name = 'create_task.html'
#     success_url = reverse_lazy('task_list')

#     def form_valid(self, form):
#         form.instance.created_by = self.request.user
#         task = form.save()

#         # Automatically assign the task to all members of the team
#         team = task.team
#         team_members = team.members.all()

#         for team_member in team_members:
#             TaskMember.objects.create(
#                 team=team,
#                 task=task,
#                 assigned_to=team_member.user,
#                 due_date=task.due_date,
#                 status='pending'
#             )

#         return super().form_valid(form)


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        try:
            task_member = TaskMember.objects.get(
                task=task, assigned_to=self.request.user)

            # Pass a flag indicating whether the user is the creator of the task
            # check for true and false
            context['is_creator'] = task_member.team.created_by == task.created_by
            context['task_member'] = task_member
        except:
            context['is_creator'] = ""
            context['task_member'] = ""
        return context

    def form_valid(self, form):
        task = form.save(commit=False)

        # Set the status field based on the form data
        status = self.request.POST.get('status', None)
        if status:
            # Get the TaskMember associated with the current user and task
            task_member = TaskMember.objects.get(
                task=task, assigned_to=self.request.user)
            task_member.status = status
            task_member.save()

        task.save()
        return super().form_valid(form)


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete_task.html'
    success_url = reverse_lazy('task_list')

    def delete(self, request, *args, **kwargs):
        # Delete associated TaskMembers before deleting the task
        task = self.get_object()
        TaskMember.objects.filter(task=task).delete()
        return super().delete(request, *args, **kwargs)


class MyTaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        # Get teams where the logged-in user is a member
        # return Task.objects.filter(member_task__assigned_to=self.request.user)
        tasks = Task.objects.filter(member_task__assigned_to=self.request.user).order_by(
            Case(
                When(priority=Task.HIGH_PRIORITY, then=0),
                When(priority=Task.LOW_PRIORITY, then=2),
                When(priority=Task.NORMAL_PRIORITY, then=1),
                default=3,  # Add a default value to handle any other priorities
                output_field=models.IntegerField(),
            )
        )
        return tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add additional context data here
        context['list_type'] = 'my_task'
        return context


class TaskMemberUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        try:
            task_member = TaskMember.objects.get(
                task=task, assigned_to=self.request.user)

            # Pass a flag indicating whether the user is the creator of the task
            # check for true and false
            context['is_creator'] = task_member.team.created_by == task.created_by
            context['task_member'] = task_member
        except:
            context['is_creator'] = ""
            context['task_member'] = ""

        # Iterate through form fields and set them as read-only
        for field_name, field in self.get_form().fields.items():
            context['form'].fields[field_name].widget.attrs['readonly'] = True
            if field_name == "team":
                context['form'].fields[field_name].choices = [(task.team.id, str(task.team))]
            elif field_name == "priority":
                context['form'].fields[field_name].choices = [(task.priority, str(task.priority))]

        return context
    
    def form_valid(self, form):
        task = form.save(commit=False)

        # Set the status field based on the form data
        status = self.request.POST.get('status', None)
        if status:
            # Get the TaskMember associated with the current user and task
            task_member = TaskMember.objects.get(
                task=task, assigned_to=self.request.user)
            task_member.status = status
            task_member.save()

        task.save()
        return super().form_valid(form)
