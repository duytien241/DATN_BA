import logging
import uuid
from typing import Any, Awaitable, Callable, Dict, Iterable, List, Optional, Text

from rasa.core.channels.channel import InputChannel, OutputChannel, UserMessage
from rasa.utils.common import raise_warning
from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse
from sccli.Socketcluster import socket
import asyncio
import threading

logger = logging.getLogger(__name__)


class SocketClusterOutput(OutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "socketcluster"

    def __init__(self, sc: socket, bot_message_evt: Text) -> None:
        self.sc = sc
        self.bot_message_evt = bot_message_evt

    async def _send_message(self, recipient_id: Text, response: Any) -> None:
        """Sends a message to the recipient using the bot event."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sc.publish, f"{self.bot_message_evt}", response)

    async def send_text_message(
        self, recipient_id: Text, text: Text, **kwargs: Any
    ) -> None:
        """Send a message through this channel."""
        for message_part in text.strip().split("\n\n"):
            await self._send_message(recipient_id, {"text": message_part})

    async def send_image_url(
        self, recipient_id: Text, image: Text, **kwargs: Any
    ) -> None:
        """Sends an image to the output"""

        message = {"attachment": {"type": "image", "payload": {"src": image}}}
        await self._send_message(recipient_id, message)

    async def send_text_with_buttons(
        self,
        recipient_id: Text,
        text: Text,
        buttons: List[Dict[Text, Any]],
        **kwargs: Any,
    ) -> None:
        """Sends buttons to the output."""

        # split text and create a message for each text fragment
        # the `or` makes sure there is at least one message we can attach the quick
        # replies to
        message_parts = text.strip().split("\n\n") or [text]
        messages = [{"text": message, "quick_replies": []}
                    for message in message_parts]

        # attach all buttons to the last text fragment
        for button in buttons:
            messages[-1]["quick_replies"].append(
                {
                    "content_type": "text",
                    "title": button["title"],
                    "payload": button["payload"],
                }
            )

        for message in messages:
            await self._send_message(recipient_id, message)

    async def send_elements(
        self, recipient_id: Text, elements: Iterable[Dict[Text, Any]], **kwargs: Any
    ) -> None:
        """Sends elements to the output."""

        for element in elements:
            message = {
                "attachment": {
                    "type": "template",
                    "payload": {"template_type": "generic", "elements": element},
                }
            }

            await self._send_message(recipient_id, message)

    async def send_custom_json(
        self, recipient_id: Text, json_message: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends custom json to the output"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.sc.publish, f"{self.bot_message_evt}", **json_message)

    async def send_attachment(
        self, recipient_id: Text, attachment: Dict[Text, Any], **kwargs: Any
    ) -> None:
        """Sends an attachment to the user."""
        await self._send_message(recipient_id, {"attachment": attachment})


class SocketClusterInput(InputChannel):
    """A socketcluster input channel."""

    @classmethod
    def name(cls) -> Text:
        return "socketcluster"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> InputChannel:
        credentials = credentials or {}
        return cls(
            credentials.get("user_message_evt", "user_uttered"),
            credentials.get("bot_message_evt", "bot_uttered"),
            credentials.get("namespace"),
            credentials.get("session_persistence", False),
            credentials.get("sc_path", "/socketcluster"),
        )

    def __init__(
        self,
        user_message_evt: Text = "user_uttered",
        bot_message_evt: Text = "bot_uttered",
        namespace: Optional[Text] = None,
        session_persistence: bool = False,
        sc_path: Optional[Text] = "ws://localhost:8000/socketcluster/",
    ):
        self.bot_message_evt = bot_message_evt
        self.session_persistence = session_persistence
        self.user_message_evt = user_message_evt
        self.namespace = namespace
        self.sc_path = sc_path
        self.sc = None

    def get_output_channel(self) -> Optional["OutputChannel"]:
        if self.sc is None:
            raise_warning(
                "Socket Cluster output channel cannot be recreated. "
                "This is expected behavior when using multiple Sanic "
                "workers or multiple Rasa Open Source instances. "
                "Please use a different channel for external events in these "
                "scenarios."
            )
            return
        return SocketClusterOutput(self.sc, self.bot_message_evt)

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        loop = asyncio.get_event_loop()

        sc = socket(self.sc_path)
        sc_webhook = Blueprint("sc_webhook", __name__)

        # make sc object static to use in get_output_channel
        self.sc = sc

        @sc_webhook.route("/", methods=["GET"])
        async def health(_: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        def onconnect(sock: socket):
            print("Connected")
            sc.subscribe(f"{self.user_message_evt}")

        def ondisconnect(sock: socket):
            print("Disconnected")

        def on_message_client(channel, obj):
            id_chanel = '1'
            print(obj)
            message = None
            if "id" in obj:
                id_chanel = obj['id']
            output = self.bot_message_evt + id_chanel
            output_channel = SocketClusterOutput(sc,  output)
            message = UserMessage(
                    text=obj['text'], output_channel=output_channel, sender_id=id_chanel, input_channel=self.name()
                )

            loop.run_until_complete(on_new_message(message))

        def on_message(channel, obj):
            print(obj)
            message = None
            if 'id' in obj:
                channel_name = self.user_message_evt + obj['id']
                if channel_name not in sc.channels:
                    sc.subscribe(f"{channel_name}")
                    sc.onchannel(f"{channel_name}", on_message_client)
            loop.run_until_complete(on_new_message(message))

        def on_connect_error(sock: socket, err):
            print("Disconnected", err)
        sc.enablereconnection = True
        sc.setBasicListener(onconnect, ondisconnect, on_connect_error)
        sc.onchannel(f"{self.user_message_evt}", on_message)
        t = threading.Thread(target=sc.connect)
        t.daemon = True
        t.start()
        return sc_webhook
