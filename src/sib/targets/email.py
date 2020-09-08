import typing as t
import smtplib

import requests
from email.message import EmailMessage

from targets.base import TargetBase


class TargetEmail(TargetBase):
    def __init__(
            self,
            domain: str,
            login: str,
            password: str,
            recipients: t.List[str],
    ):
        self._smtp = smtplib.SMTP()
        self._smtp.connect(domain, '587')
        self._login = login
        self._recipients = recipients
        self._smtp.login(login, password)

    def handle(self, request: requests.Request):
        subject = 'forwarded'
        content = str(request.data)
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self._login
        msg['To'] = ', '.join(self._recipients)
        self._smtp.send_message(msg)

    def close(self):
        self._smtp.quit()
