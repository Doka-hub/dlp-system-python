

class BaseDateErrorText:
    text = None


class TextDataFoundErrorText(BaseDateErrorText):
    text = '_- Сообщение содержало потенциально важные данные._'


class FileDataFoundErrorText(BaseDateErrorText):
    text = '\n_- Некоторые файлы содержали потенциально важные данные._'
