from apps.dlp.dlp_component.data_search.files import (
    BaseFilesDataSearch,

    NotSupportedFileDataSearch,
    CsvFileDataSearch,
    DocxFileDataSearch,
    TxtFileDataSearch,
)
from apps.dlp.dlp_component.slack_.mixins import SlackFileIdMixin


class SlackNotSupportedFileDataSearch(
    SlackFileIdMixin,
    NotSupportedFileDataSearch,
):
    pass


class SlackCsvFileDataSearch(SlackFileIdMixin, CsvFileDataSearch):
    pass


class SlackDocxFileDataSearch(SlackFileIdMixin, DocxFileDataSearch):
    pass


class SlackTxtFileDataSearch(SlackFileIdMixin, TxtFileDataSearch):
    pass


class SlackFilesDataSearch(BaseFilesDataSearch):

    def find_data(self, pattern: str):
        return [
            file_data_search for file_data_search in self.file_data_search_list
            if file_data_search.find_data(pattern)
        ]

