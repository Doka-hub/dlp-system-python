from django.urls import path

from .views import EventAPIView


urlpatterns = [
    path('slack-event/', EventAPIView.as_view(), name='slack-event'),
]
