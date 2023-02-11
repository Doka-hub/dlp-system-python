from abc import abstractmethod

import re


class BaseFileDataSearch:
    FILE_TYPES = None

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


class NotSupportedFileDataSearch(BaseFileDataSearch):

    def get_decoded_file_bytes(self):
        return ''

    def find_data(self, *args, **kwargs):
        return


class XlsxFileDataSearch(BaseFileDataSearch):
    FILE_TYPES = ('xlsx',)

    def get_decoded_file_bytes(self):
        return ''

    def find_data(self, pattern):
        return


class CsvFileDataSearch(BaseFileDataSearch):
    FILE_TYPES = ('csv',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())


class DocxFileDataSearch(BaseFileDataSearch):
    FILE_TYPES = ('docx',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())


class TxtFileDataSearch(BaseFileDataSearch):
    FILE_TYPES = ('txt',)

    def get_decoded_file_bytes(self):
        return self.file_bytes.decode()

    def find_data(self, pattern: str):
        return re.findall(pattern, self.get_decoded_file_bytes())
