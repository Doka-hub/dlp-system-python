from pydantic import BaseModel


class SlackFileModel(BaseModel):
    id: str
    download_url: str
    filename: str
    bytes: bytes | None

    @property
    def filetype(self):
        return self.filename[self.filename.rfind('.') + 1:]


class SlackRequestEventModel(BaseModel):
    channel: str
    channel_type: str
    event_ts: str

    message: dict | None

    text: str | None
    files: list[SlackFileModel] | None

    type: str
    subtype: str | None
    user: str | None

    @property
    def chat_update_ts(self):
        if self.message:
            ts = self.message['ts']
        else:
            ts = self.event_ts
        return ts


class SlackRequestModel(BaseModel):
    token: str
    team_id: str | None
    api_app_id: str | None

    event: SlackRequestEventModel | None
    type: str
    event_context: str | None
    event_id: str | None
    event_time: int | None

    challenge: str | None
