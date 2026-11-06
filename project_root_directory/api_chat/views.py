from rest_framework import generics, permissions
from rest_framework.response import Response

from app_chatbot.utils.graph import respond
from app_core.models import Chat
from api_chat.serializers import ChatSerializer


class ChatView(generics.ListCreateAPIView):
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user).order_by('created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']
        chat = Chat.objects.create(
            user=request.user, message=message, response=respond(message))
        return Response(self.get_serializer(chat).data, status=201)
