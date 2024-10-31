from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Team, Membership
from users.models import Profile

User = get_user_model()

class BaseTestSetup(TestCase):
    def setUp(self):
        # Shared setup for coach, second coach, and player users
        self.coach_user = User.objects.create_user(username="coach_user", password="password123")
        Profile.objects.create(user=self.coach_user, role="coach")

        self.coach_user2 = User.objects.create_user(username="coach_user2", password="password123")
        Profile.objects.create(user=self.coach_user2, role="coach")

        self.player_user = User.objects.create_user(username="player_user", password="password123")
        Profile.objects.create(user=self.player_user, role="player")

        self.team1 = Team.objects.create(name="Team 1", coach=self.coach_user)
        self.team2 = Team.objects.create(name="Team 2", coach=self.coach_user2)


class CreateTeamViewTests(BaseTestSetup):
    
    def test_non_coach_access(self):
        self.client.login(username="player_user", password="password123")
        response = self.client.get(reverse('create_team'))
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Only coaches can create teams." in str(msg) for msg in messages))
    
    def test_team_creation_without_name(self):
        self.client.login(username="coach_user", password="password123")
        response = self.client.post(reverse('create_team'), {'name': ''})
        
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Please enter a team name." in str(msg) for msg in messages))
    
    def test_coach_with_existing_team(self):
        self.client.login(username="coach_user", password="password123")
        
        Team.objects.create(name="Existing Team", coach=self.coach_user)
        response = self.client.get(reverse('create_team'))
        
        self.assertRedirects(response, reverse('manage_team'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You already have a team." in str(msg) for msg in messages))

    def test_successful_team_creation(self):
        self.client.login(username="coach_user", password="password123")
        
        response = self.client.post(reverse('create_team'), {'name': 'New Team'})
        
        self.assertRedirects(response, reverse('manage_team'))
        self.assertTrue(Team.objects.filter(name="New Team", coach=self.coach_user).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Team 'New Team' created successfully." in str(msg) for msg in messages))


class ManageRequestsViewTests(BaseTestSetup):

    def test_manage_requests_no_team(self):
        self.client.login(username="coach_user", password="password123")
        response = self.client.get(reverse('pending_requests'))
        
        self.assertRedirects(response, reverse('create_team'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You need to create a team first." in str(msg) for msg in messages))

    def test_manage_requests_with_team(self):
        team = Team.objects.create(name="Team A", coach=self.coach_user)
        Membership.objects.create(team=team, player=self.player_user, status=Membership.PENDING)

        self.client.login(username="coach_user", password="password123")
        response = self.client.get(reverse('pending_requests'))

        self.assertEqual(response.status_code, 200)

class TeamListViewTests(BaseTestSetup):
    def setUp(self):
        super().setUp()
        Membership.objects.create(team=self.team1, player=self.player_user, status=Membership.APPROVED)

    def test_team_list_excludes_joined_teams(self):
        self.client.login(username="player_user", password="password123")
        response = self.client.get(reverse('team_list'))

        self.assertEqual(response.status_code, 200)

        teams = response.context['teams']

        self.assertIn(self.team2, teams)

        # Player is in team1 so should not be shown
        self.assertNotIn(self.team1, teams)