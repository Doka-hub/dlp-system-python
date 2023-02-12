from abc import abstractmethod, ABCMeta

from apps.dlp.dlp_component.data_search.files import (
    NotSupportedFileDataSearch,
)


class BaseMessageController(metaclass=ABCMeta):
    text_data_search_class = None
    files_data_search_class = None
    file_data_search_classes = None
    not_supported_file_data_search_class = NotSupportedFileDataSearch

    def get_files_data_search_class(self):
        assert self.files_data_search_class is not None, (
            f"'{self.__class__.__name__}' should either include a `files_data_search_class` attribute."
        )
        return self.files_data_search_class

    def get_text_data_search_class(self):
        assert self.text_data_search_class is not None, (
            f"'{self.__class__.__name__}' should either include a `text_data_search_class` attribute."
        )
        return self.text_data_search_class

    def get_file_data_search_class(self, filetype: str):
        assert self.file_data_search_classes is not None, (
            f"'{self.__class__.__name__}' should either include a `file_data_search_classes` attribute."
        )

        file_data_search_class = self.not_supported_file_data_search_class

        for class_ in self.file_data_search_classes:
            if filetype in class_.file_types:
                file_data_search_class = class_
                break

        return file_data_search_class

    @abstractmethod
    def find_data(self):
        raise NotImplementedError()
