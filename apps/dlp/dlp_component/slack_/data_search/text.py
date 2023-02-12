import re

from apps.dlp.dlp_component.data_search.text import BaseTextDataSearch


class SlackTextDataSearch(BaseTextDataSearch):

    def find_data(self, pattern: str):
        if self.text:
            return re.findall(pattern, self.text)
