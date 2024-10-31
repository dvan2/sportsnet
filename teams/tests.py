from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Team
from users.models import Profile

User = get_user_model()

class CreateTeamViewTests(TestCase):
    def setUp(self):
        self.coach_user = User.objects.create_user(username="coach_user", password="passwrod")
        Profile.objects.create(user=self.coach_user, role="coach")

        self.player_user = User.objects.create_user(username="player_user", password="password")
        Profile.objects.create(user=self.player_user, role="player")
    
    def test_non_coach_access(self):
        self.client.login(username="player_user", password="password")
        response = self.client.get(reverse('create_team'))

        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Only coaches can create teams." in str(msg) for msg in messages))
    
    def test_coach_with_existing_team(self):
        self.client.login(username="coach_user", password="password123")
        
        # Create a team for the coach user
        Team.objects.create(name="Existing Team", coach=self.coach_user)
        
        response = self.client.get(reverse('create_team'))
        
        # Check that the coach is redirected to the manage team page
        self.assertRedirects(response, reverse('manage_team'))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("You already have a team." in str(msg) for msg in messages))
    
    def test_team_creation_without_name(self):
        self.client.login(username="coach_user", password="password123")
        
        response = self.client.post(reverse('create_team'), {'name': ''})
        
        # Check that the response contains the error message
        self.assertEqual(response.status_code, 200)  # Stay on the same page
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Please enter a team name." in str(msg) for msg in messages))
    
    def test_successful_team_creation(self):
        self.client.login(username="coach_user", password="password123")
        
        response = self.client.post(reverse('create_team'), {'name': 'New Team'})
        
        # Check that the team was created successfully
        self.assertRedirects(response, reverse('manage_team'))
        self.assertTrue(Team.objects.filter(name="New Team", coach=self.coach_user).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Team 'New Team' created successfully." in str(msg) for msg in messages))


