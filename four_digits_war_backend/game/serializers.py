from rest_framework import serializers
from .models import Game, Guess

class GuessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = '__all__'
        read_only_fields = ('picas', 'fijas', 'created_at', 'player')

class GameSerializer(serializers.ModelSerializer):
    guesses = GuessSerializer(many=True, read_only=True)
    class Meta:
        model = Game
        fields = '__all__'
        read_only_fields = ('player1', 'current_turn', 'winner', 'is_finished', 'created_at')

    def validate_player1_secret(self, value):
        if len(value) != 4 or not value.isdigit():
            raise serializers.ValidationError("player1_secret must be exactly 4 digits.")
        if len(set(value)) != 4:
            raise serializers.ValidationError("Digits in player1_secret must be unique.")
        return value
    
    def validate(self, attrs):
        # Impedir que player2_secret venga en la creación
        if 'player2_secret' in attrs:
            raise serializers.ValidationError("player2_secret should not be set on game creation.")
        return attrs      

class GuessSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guess
        fields = ['guess_number']
