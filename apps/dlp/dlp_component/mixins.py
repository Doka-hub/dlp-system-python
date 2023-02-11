from django.conf import settings

import requests


class SlackFileIdMixin:
    def __init__(
        self,
        file_id: str,
        file_bytes: bytes,
        filename: str,
        filetype: str,
        *args,
        **kwargs,
    ):
        super().__init__(file_bytes, filename, filetype, *args, **kwargs)
        self.id = file_id


class SlackGetFileBytesByURLMixin:

    @staticmethod
    def get_file_bytes_from_url(url: str):
        response = requests.get(
            url,
            headers={
                'Authorization': f'Bearer {settings.SLACK_USER_TOKEN}',
            },
        )
        return response.content
