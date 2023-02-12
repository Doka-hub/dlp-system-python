from django.conf import settings

import slack

from apps.dlp.dlp_component.slack_.data_search.files import (
    SlackCsvFileDataSearch,
    SlackDocxFileDataSearch,
    SlackTxtFileDataSearch,

    SlackFilesDataSearch,
)
from apps.dlp.dlp_component.slack_.data_search.text import SlackTextDataSearch
from apps.dlp.dlp_component.slack_.message_controller import (
    BaseSlackMessageController,
)

from apps.dlp.dlp_component.error_texts import (
    TextDataFoundErrorText,
    FileDataFoundErrorText,
)
from apps.dlp.models import ReTemplate

from .utils import (
    get_clean_file_ids,
    get_slack_message,
    create_slack_files,
)


class SlackMessageController(BaseSlackMessageController):
    ALLOWED_EVENT_TYPES = ['message']

    text_data_search_class = SlackTextDataSearch
    files_data_search_class = SlackFilesDataSearch
    file_data_search_classes = (
        SlackCsvFileDataSearch,
        SlackDocxFileDataSearch,
        SlackTxtFileDataSearch,
    )

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
                as_user=True,
                **message_data,
            )

    @property
    def is_allowed_event_type(self):
        return self.data.event.type in self.ALLOWED_EVENT_TYPES

    def get_new_text(self, text_data, files_data):
        new_text = None

        if text_data:
            new_text = TextDataFoundErrorText.text

        if files_data:
            if new_text:
                new_text = f'{new_text} {FileDataFoundErrorText.text}'
            else:
                new_text = (
                    f'{self.data.event.text} {FileDataFoundErrorText.text}'
                )

        return new_text

    def find_data(self):
        text_data_search_class = self.get_text_data_search_class()
        files_data_search_class = self.get_files_data_search_class()

        text_data_search = text_data_search_class(self.data.event.text)
        files_data_search = files_data_search_class(
            self.get_file_data_search_list(),
        )

        slack_message = get_slack_message(self.data)

        re_templates = ReTemplate.objects.all()
        for re_template in re_templates:
            text_data = text_data_search.find_data(re_template.rpattern)
            files_data_search_list = files_data_search.find_data(
                re_template.rpattern
            )

            # если найдены данные
            if text_data or files_data_search_list:
                # если сообщение еще не сохранено
                if not slack_message.id:
                    slack_message.save()

                slack_message.re_templates.add(re_template)

                new_text = self.get_new_text(text_data, files_data_search_list)
                file_ids = None

                if files_data_search_list:
                    file_ids = get_clean_file_ids(
                        self.data,
                        [file_data.id for file_data in files_data_search_list],
                    )

                    slack_file_list = create_slack_files(
                        files_data_search_list
                    )

                    slack_message.files.add(*slack_file_list)

                self.edit_message(new_text, file_ids)
