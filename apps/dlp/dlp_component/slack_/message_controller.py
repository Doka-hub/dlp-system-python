from abc import ABCMeta

from apps.dlp.dlp_component.message_controller import BaseMessageController
from apps.slack_.events.models import SlackRequestModel

from .data_search.files import SlackNotSupportedFileDataSearch
from .mixins import SlackGetFileBytesByURLMixin


class BaseSlackMessageController(
    SlackGetFileBytesByURLMixin,
    BaseMessageController,
    metaclass=ABCMeta,
):
    not_supported_file_data_search_class = SlackNotSupportedFileDataSearch

    def __init__(
        self,
        token: str,
        team_id: str | None,
        api_app_id: str | None,
        event: dict | None,
        type: str,
        event_context: str | None,
        event_id: str | None,
        event_time: int | None,
        challenge: str | None = None,
    ):
        self.data = SlackRequestModel(
            token=token,
            team_id=team_id,
            api_app_id=api_app_id,
            event=event,
            type=type,
            event_context=event_context,
            event_id=event_id,
            event_time=event_time,
            challenge=challenge,
        )

    def get_file_data_search_list(self):
        file_data_search_list = []

        for file in self.data.event.files:
            file.bytes = self.get_file_bytes_from_url(file.download_url)
            file_data_search_class = self.get_file_data_search_class(
                file.filetype
            )
            file_data_search_list.append(
                file_data_search_class(
                    file.id,
                    file.bytes,
                    file.filename,
                    file.filetype,
                )
            )

        return file_data_search_list
