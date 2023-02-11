from rest_framework import serializers


class SlackRequestEventFileSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    download_url = serializers.SerializerMethodField(allow_null=True)
    filename = serializers.SerializerMethodField(allow_null=True)

    def get_download_url(self, data: dict):
        return data.get('url_private_download')

    def get_filename(self, data: dict):
        return data.get('name')


class SlackRequestEventSerializer(serializers.Serializer):
    channel = serializers.CharField(max_length=255)
    channel_type = serializers.CharField(max_length=255)
    event_ts = serializers.CharField(max_length=255)

    message = serializers.DictField(allow_null=True)

    text = serializers.CharField(max_length=255, allow_null=True)
    files = SlackRequestEventFileSerializer(many=True, default=[])

    type = serializers.CharField(max_length=255)
    subtype = serializers.CharField(max_length=255, allow_null=True)
    user = serializers.CharField(max_length=255, allow_null=True)


class SlackRequestSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    team_id = serializers.CharField(max_length=255, allow_null=True)
    api_app_id = serializers.CharField(max_length=255, allow_null=True)

    event = SlackRequestEventSerializer(allow_null=True)
    type = serializers.CharField(max_length=255)
    event_context = serializers.CharField(max_length=255, allow_null=True)
    event_id = serializers.CharField(max_length=255, allow_null=True)
    event_time = serializers.IntegerField(allow_null=True)

    challenge = serializers.CharField(default=None)
