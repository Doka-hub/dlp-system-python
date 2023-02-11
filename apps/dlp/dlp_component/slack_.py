from abc import ABCMeta, abstractmethod

from django.conf import settings

import re

import slack

from apps.slack_.events.models import SlackRequestModel

from .base import BaseDataSearch, BaseMessageController
from .files import (
    NotSupportedFileDataSearch,
    XlsxFileDataSearch,
    CsvFileDataSearch,
    DocxFileDataSearch,
    TxtFileDataSearch,
)
from .mixins import SlackFileIdMixin, SlackGetFileBytesByURLMixin


class SlackNotSupportedFileDataSearch(
    SlackFileIdMixin,
    NotSupportedFileDataSearch,
):
    pass


class SlackXlsxFileDataSearch(SlackFileIdMixin, XlsxFileDataSearch):
    pass


class SlackCsvFileDataSearch(SlackFileIdMixin, CsvFileDataSearch):
    pass


class SlackDocxFileDataSearch(SlackFileIdMixin, DocxFileDataSearch):
    pass


class SlackTxtFileDataSearch(SlackFileIdMixin, TxtFileDataSearch):
    pass


class BaseSlackMessageController(
    SlackGetFileBytesByURLMixin,
    BaseMessageController,
    metaclass=ABCMeta,
):

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

    def edit_message(
        self,
        new_text: str | None,
        file_ids: list[str] | None = None,
    ) -> None:
        """
        Изменяет сообщение, если указан хоть один пункт:
            - new_text
            - file_ids

        :param new_text: новый текст
        :param file_ids: список новых файлов (запрещенные удалены)
        :return:
        """
        message_data = {}
        if new_text and new_text != '':
            message_data['text'] = new_text
        if file_ids is not None:
            message_data['file_ids'] = file_ids

        if message_data:
            client = slack.WebClient(settings.SLACK_USER_TOKEN)
            client.chat_update(
                channel=self.data.event.channel,
                ts=self.data.event.chat_update_ts,
                **message_data,
            )


class SlackDataSearch(BaseDataSearch):
    def regex_text_findall(self, pattern: str):
        if self.text:
            return re.findall(pattern, self.text)

    def regex_files_findall(self, pattern: str):
        if self.files:
            return [file for file in self.files if file.find_data(pattern)]
