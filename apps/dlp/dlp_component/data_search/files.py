from abc import abstractmethod, ABCMeta

import re


class BaseFileDataSearch(metaclass=ABCMeta):
    file_types = tuple()

    def __init__(self, file_bytes: bytes, filename: str, filetype: str):
        self.file_bytes = file_bytes
        self.filename = filename
        self.filetype = filetype

    @abstractmethod
    def get_decoded_file_bytes(self):
        raise NotImplementedError()

    @abstractmethod
    def find_data(self, *args, **kwargs):
        """
        Для каждого типа файлов нужен свой метод поиска

        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplementedError()


class BaseFilesDataSearch:
    def __init__(self, file_data_search_list: list[BaseFileDataSearch]):
        self.file_data_search_list = file_data_search_list

    def find_data(self, *args, **kwargs):
        return [
            file_data_search.find_data(*args, **kwargs)
            for file_data_search in self.file_data_search_list
        ]


class NotSupportedFileDataSearch(BaseFileDataSearch):

    def get_decoded_file_bytes(self):
        return ''

    def find_data(self, *args, **kwargs):
        return


class CsvFileDataSearch(BaseFileDataSearch):
    file_types = ('csv',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())


class DocxFileDataSearch(BaseFileDataSearch):
    file_types = ('docx',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())


class TxtFileDataSearch(BaseFileDataSearch):
    file_types = ('txt',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())
