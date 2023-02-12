from django.core.files.base import ContentFile

from apps.slack_.models import SlackFile, SlackMessage


def get_clean_file_ids(data, bad_file_ids: list[str]):
    file_ids = [file.id for file in data.event.files]
    file_ids = list(set(file_ids) - set(bad_file_ids))
    return file_ids


def get_slack_message(data):
    return SlackMessage(
        text=data.event.text,
        date=data.event.date,
        time=data.event.time,
        team_id=data.team_id,
        channel_id=data.event.channel,
        owner_id=data.event.user,
    )


def create_slack_files(files_data):
    return [
        SlackFile.objects.create(
            file=ContentFile(
                file_data_search.file_bytes,
                file_data_search.filename,
            ),
            filetype=file_data_search.filetype,
            filename=file_data_search.filename,
        ) for file_data_search in files_data
    ]
