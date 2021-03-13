import requests
import json

from enum import Enum

from requests import Response

DEFAULT_USERNAME = "Python Slack Notifications"
DEFAULT_ICON_EMOJI = "slack"


class Color(Enum):
    SUCCESS = "#00b600"
    INFO = "#7799b9"
    ERROR = "#ef0000"
    WARNING = "#ffce03"


class Icon(Enum):
    SUCCESS = "white_check_mark"
    INFO = "information_source"
    ERROR = "x"
    WARNING = "warning"


class NotificationService:
    """
    Provides convenience methods for formatting of different types of messages sent to slack,
    including success(), info(), warning(), and error()
    """

    def __init__(self, webhook: str, username: str = DEFAULT_USERNAME, icon_emoji: str = DEFAULT_ICON_EMOJI):
        """
        Includes configuration for successful setup to use slack webhook
        webhook is the only required parameter - others will default
        :param webhook: REQUIRED - must be set up in Slack
        :param username: OPTIONAL - defaults to 'Python Slack Notifications'
        :param icon_emoji: OPTIONAL - defaults to 'slack'
        """
        self.webhook = webhook
        self.username = username
        self.icon_emoji = icon_emoji

    BASE_SLACK_URL = "https://hooks.slack.com/services/"

    def slack_payload_with_attachments(self, attachments):
        return json.dumps({
            "username": self.username,
            "icon_emoji": f":{self.icon_emoji}:",
            "unfurl_links": True,
            "attachments": attachments
        })

    @property
    def slack_url(self):
        return self.BASE_SLACK_URL + self.webhook

    @staticmethod
    def setup_fallback(icon: str, title: str, link: str = None, link_title: str = "link"):
        """
        helper method
        :param icon:
        :param title:
        :param link: OPTIONAL
        :param link_title: OPTIONAL - if link is supplied, link_title defaults to 'link'
        :return:
        """
        if link:
            if link_title is None:
                link_title = "link"
            fallback = f" :{icon}: *{title}*: (<{link}|{link_title}>)"
        else:
            fallback = f" :{icon}: *{title}*"
        return fallback

    @staticmethod
    def setup_attachments(color: str, fallback: str, message: str):
        """
        helper method - all parameters required for successful configuration of payload
        :param color:
        :param fallback:
        :param message:
        :return:
        """
        return [
            {
                "fallback": fallback,
                "color": color,
                "fields": [
                    {
                        "value": f"{fallback}\n{message}",
                        "short": False
                    }
                ]
            }
        ]

    def send_msg(self, title: str, msg_color: Color, msg_icon: Icon, message: str, link: str = None,
                 link_title: str = None) -> Response:
        """

        :param title:
        :param msg_color:
        :param msg_icon:
        :param message:
        :param link:
        :param link_title:
        :return:
        """
        fallback = self.setup_fallback(msg_icon.value, title, link, link_title)
        attachments = self.setup_attachments(msg_color.value, fallback, message)
        return requests.post(self.slack_url,
                      data={"payload": self.slack_payload_with_attachments(attachments)})

    def success(self, title: str, message: str = "Success!", link: str = None, link_title: str = None) -> Response:
        """
        Sends success message using COLOR_SUCCESS and ICON_SUCCESS
        :param title:
        :param message:
        :param link:
        :param link_title:
        :return:
        """
        return self.send_msg(title, Color.SUCCESS, Icon.SUCCESS, message, link, link_title)

    def info(self, title: str, message: str, link: str = None, link_title: str = None) -> Response:
        """
        Sends informational message using COLOR_INFO and ICON_INFO
        :param title:
        :param message:
        :param link:
        :param link_title:
        :return:
        """
        return self.send_msg(title, Color.INFO, Icon.INFO, message, link, link_title)

    def error(self, title: str, message: str, link: str = None, link_title: str = None) -> Response:
        """
        Sends error message using COLOR_ERROR and ICON_ERROR
        :param title:
        :param message:
        :param link:
        :param link_title:
        :return:
        """
        return self.send_msg(title, Color.ERROR, Icon.ERROR, message, link, link_title)

    def warning(self, title: str, message: str, link: str = None, link_title: str = None) -> Response:
        """
        Sends informational message using COLOR_WARNING and ICON_WARNING
        :param title:
        :param message:
        :param link:
        :param link_title:
        :return:
        """
        return self.send_msg(title, Color.WARNING, Icon.WARNING, message, link, link_title)
