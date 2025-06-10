from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Game, Guess
from .serializers import GameSerializer, GuessSerializer
from .utils import count_picas_fijas
from authentication.models import User

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Al crear el juego, current_turn es el jugador 1 y solo player1_secret es obligatorio
        serializer.save(player1=self.request.user, current_turn=self.request.user, player2_secret="")

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        game = self.get_object()
        user = request.user
        if game.player2:
            return Response({'detail': 'Game already has 2 players'}, status=status.HTTP_400_BAD_REQUEST)
        if user == game.player1:
            return Response({'detail': 'Player1 cannot join as player2'}, status=status.HTTP_400_BAD_REQUEST)

        secret = request.data.get('player2_secret')
        if not secret or len(secret) != 4 or not secret.isdigit():
            return Response({'detail': 'Invalid secret. It must be exactly 4 digits.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if len(set(secret)) != 4:
            return Response({'detail': 'Secret must have unique digits, no repeats allowed.'}, status=status.HTTP_400_BAD_REQUEST)

        game.player2 = user
        game.player2_secret = secret
        game.save()
        return Response(GameSerializer(game).data)

    @action(detail=True, methods=['post'])
    def guess(self, request, pk=None):
        game = self.get_object()
        user = request.user

        if game.is_finished:
            return Response({'detail': 'Game is already finished'}, status=status.HTTP_400_BAD_REQUEST)

        if user != game.current_turn:
            return Response({'detail': 'Not your turn'}, status=status.HTTP_403_FORBIDDEN)

        if user != game.player1 and user != game.player2:
            return Response({'detail': 'You are not a player in this game'}, status=status.HTTP_403_FORBIDDEN)

        guess_number = request.data.get('guess_number')
        if not guess_number or len(guess_number) != 4 or not guess_number.isdigit():
            return Response({'detail': 'Invalid guess number. Must be exactly 4 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        # Identificar el secreto del adversario
        target = game.player2_secret if user == game.player1 else game.player1_secret

        picas, fijas = count_picas_fijas(target, guess_number)

        # Guardar el intento
        Guess.objects.create(game=game, player=user, guess_number=guess_number, picas=picas, fijas=fijas)

        if fijas == 4:
            game.winner = user
            game.is_finished = True
            game.current_turn = None
        else:
            # Cambiar turno
            game.current_turn = game.player2 if user == game.player1 else game.player1

        game.save()
        return Response({'picas': picas, 'fijas': fijas, 'game_over': game.is_finished})
