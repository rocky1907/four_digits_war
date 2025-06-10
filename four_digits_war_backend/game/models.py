from django.db import models
from authentication.models import User

class Game(models.Model):
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games_as_player2', null=True, blank=True)
    player1_secret = models.CharField(max_length=4)
    player2_secret = models.CharField(max_length=4, blank=True)
    current_turn = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_turn_games')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    guess_number = models.CharField(max_length=4)
    picas = models.IntegerField()
    fijas = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
