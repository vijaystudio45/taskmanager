from django.test import TestCase
from .models import Team, TeamMember, User

class TeamTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create(username="@test_user", password="1234567", email="test@gmail.com")
        self.team = Team.objects.create(name="Test_team", description="this is a test team", created_by=test_user)
        self.team_mem = TeamMember.objects.create(team=self.team, user=test_user)

    def test_team_member_added(self):
        # Adding a new user to the team
        new_user = User.objects.create(username="@new_user", password="password123", email="newuser@gmail.com")
        new_team_member = TeamMember.objects.create(team=self.team, user=new_user)

        # Retrieving the team again from the database
        updated_team = Team.objects.get(name="Test_team")

        # Checking if the new user is now a member of the team
        self.assertIn(new_team_member, updated_team.members.all())
