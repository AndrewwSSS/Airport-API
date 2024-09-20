from typing import Iterable

import httpx
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
        message_pattern = "You have flight tomorrow\n{0}\nDeparture time: {1}"

        self._send_notifications(
            message_pattern.format(ticket.flight.route, ticket.flight.departure_time)
            for ticket in tickets
        )
