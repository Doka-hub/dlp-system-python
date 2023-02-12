from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.slack_.serializers import SlackRequestSerializer

from .tasks import find_data


class EventAPIView(GenericAPIView):
    serializer_class = SlackRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.data)
        data = serializer.data

        find_data.delay(**data)

        return Response(data['challenge'])
