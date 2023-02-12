from dlp_system.celery import celery_app

from apps.slack_.events import SlackMessageController


@celery_app.task(name='find_data')
def find_data(**data):
    message_controller = SlackMessageController(**data)
    if message_controller.is_allowed_event_type:
        message_controller.find_data()
