import logging
import os
import smtplib
import typing as t
from email.message import EmailMessage

from sib.targets.base import TargetBase
from sib.targets.registered_targets import register_target

logger = logging.getLogger()


@register_target
class TargetEmail(TargetBase):
    QUEUE = 'email'

    @classmethod
    def create(cls):
        return cls(
            domain=os.environ['TARGET_EMAIL_DOMAIN'],
            login=os.environ['TARGET_EMAIL_LOGIN'],
            password=os.environ['TARGET_EMAIL_PASSWORD'],
            recipients=os.environ['TARGET_EMAIL_RECIPIENTS'].split(','),
        )

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

    def handle(self, headers: t.List[t.Tuple[str, str]], data: str):
        subject = 'forwarded'
        msg = EmailMessage()
        content = f'{headers=} {data=}'
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = self._login
        msg['To'] = ', '.join(self._recipients)
        logger.info(f'send {subject=} {content=}')
        self._smtp.send_message(msg)

    def close(self):
        self._smtp.quit()
