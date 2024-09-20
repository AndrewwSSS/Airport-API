from typing import Iterable

import httpx
from django.conf import settings
from django.utils import timezone

from core.models import Ticket


class NotificationService:
    def __init__(self, bot_token: str, chat_id: int):
        self.bot_token = bot_token
        self.chat_id = chat_id

    def _send_notification(self, client: httpx.Client, message: str) -> None:
        client.post(
            url=f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            data={"chat_id": self.chat_id, "text": message},
        )

    def send_notification(self, message: str) -> None:
        with httpx.Client() as client:
            self._send_notification(client, message)

    def _send_notifications(self, messages: Iterable[str]) -> None:
        with httpx.Client() as client:
            for message in messages:
                self._send_notification(client, message)

    def send_reminiscent_notification(self) -> None:
        tomorrow = timezone.now().date() + timezone.timedelta(days=1)
        tickets = Ticket.objects.filter(
            flight__departure_time__date=tomorrow,
        )

        self._send_notifications(
            settings.REMINISCENT_NOTIFICATION_MESSAGE_PATTERN.format(
                route=ticket.flight.route, departure_time=ticket.flight.departure_time
            )
            for ticket in tickets
        )
