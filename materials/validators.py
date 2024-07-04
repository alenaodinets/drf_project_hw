import re
from rest_framework import serializers


class VideoLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile("youtube.com")
        tmp = dict(value).get(self.field)
        if not bool(reg.match(tmp)):
            raise serializers.ValidationError("Указана неверная ссылка")
