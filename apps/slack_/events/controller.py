from django.core.files.base import ContentFile

from datetime import datetime

from apps.dlp.dlp_component.slack_ import (
    SlackXlsxFileDataSearch,
    SlackCsvFileDataSearch,
    SlackDocxFileDataSearch,
    SlackTxtFileDataSearch,

    SlackDataSearch,
    BaseSlackMessageController,
)
from apps.dlp.dlp_component.errors import (
    TextDataFoundErrorText,
    FileDataFoundErrorText,
)
from apps.dlp.models import ReTemplate
from apps.slack_.models import SlackFile, SlackMessage


class SlackMessageController(BaseSlackMessageController):
    FILE_DATA_SEARCH_CLASSES = (
        SlackXlsxFileDataSearch,
        SlackCsvFileDataSearch,
        SlackDocxFileDataSearch,
        SlackTxtFileDataSearch,
    )
    ALLOWED_EVENT_TYPES = ['message']

    def get_clean_file_ids(self, bad_file_ids: list[str]):
        file_ids = [file.id for file in self.data.event.files]
        file_ids = list(set(file_ids) - set(bad_file_ids))
        return file_ids

    def find_data(self):
        if self.data.event.type in self.ALLOWED_EVENT_TYPES:
            files = self.get_file_data_search_list()
            datetime_ = datetime.fromtimestamp(float(self.data.event.event_ts))

            re_templates = ReTemplate.objects.all()
            for re_template in re_templates:
                slack_data_search = SlackDataSearch(
                    text=self.data.event.text,
                    files=files,
                )
                text_data = slack_data_search.regex_text_findall(
                    re_template.pattern
                )
                file_data_search_list = slack_data_search.regex_files_findall(
                    re_template.pattern
                )

                new_text = None
                file_ids = None

                slack_message = SlackMessage(
                    re_template=re_template,
                    text=self.data.event.text,
                    date=datetime_.date(),
                    time=datetime_.time(),
                    team_id=self.data.team_id,
                    channel_id=self.data.event.channel,
                    owner_id=self.data.event.user,
                )

                if text_data:
                    new_text = TextDataFoundErrorText.text

                    slack_message.save()

                if file_data_search_list:
                    file_ids = self.get_clean_file_ids(
                        [file_data.id for file_data in file_data_search_list]
                    )

                    if new_text:
                        new_text = new_text + FileDataFoundErrorText.text
                    else:
                        new_text = (
                            self.data.event.text + FileDataFoundErrorText.text
                        )

                    slack_file_list = [
                        SlackFile.objects.create(
                            file=ContentFile(
                                file_data_search.file_bytes,
                                file_data_search.filename,
                            ),
                            filetype=file_data_search.filetype,
                            filename=file_data_search.filename,
                        ) for file_data_search in file_data_search_list
                    ]

                    if not slack_message.id:
                        slack_message.save()

                    slack_message.files.add(*slack_file_list)

                self.edit_message(new_text, file_ids)
