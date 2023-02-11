from abc import abstractmethod

from .files import (
    NotSupportedFileDataSearch,
    XlsxFileDataSearch,
    CsvFileDataSearch,
    DocxFileDataSearch,
    TxtFileDataSearch,
)


class BaseDataSearch:
    def __init__(
        self,
        *,
        text: str | None,
        files: list[
                   NotSupportedFileDataSearch,
                   XlsxFileDataSearch,
                   CsvFileDataSearch,
                   DocxFileDataSearch,
                   TxtFileDataSearch,
               ] | None = None
    ):
        self.text = text
        self.files = files

    @abstractmethod
    def regex_text_findall(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def regex_files_findall(self, *args, **kwargs):
        raise NotImplementedError()


class BaseMessageController:
    FILE_DATA_SEARCH_CLASSES = None

    def get_file_data_search_class(self, filetype: str):
        file_data_search_class = NotSupportedFileDataSearch

        for FILE_DATA_SEARCH_CLASS in self.FILE_DATA_SEARCH_CLASSES:
            if filetype in FILE_DATA_SEARCH_CLASS.FILE_TYPES:
                file_data_search_class = FILE_DATA_SEARCH_CLASS
                break

        return file_data_search_class

    @abstractmethod
    def find_data(self):
        raise NotImplementedError()
