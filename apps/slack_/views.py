from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.slack_.events import SlackMessageController
from apps.slack_.serializers import SlackRequestSerializer


class EventAPIView(GenericAPIView):
    serializer_class = SlackRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = SlackRequestSerializer(request.data)
        data = serializer.data

        event_controller = SlackMessageController(**serializer.data)
        event_controller.find_data()

        return Response(data['challenge'])
