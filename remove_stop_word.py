from rasa.nlu.components import Component
from rasa.nlu.training_data import Message
import typing
from typing import Any, Optional, Text, Dict
from rasa_sdk.events import FollowupAction, SlotSet

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class SpellCorrection(Component):

    provides = ["text"]
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(SpellCorrection, self).__init__(component_config)

    def process(self, message, **kwargs):
        mt =  message.text
        stocks = []
        with open('resources/stock.txt', 'r', encoding='utf8') as f:
            for line in f:
                stocks.append(line.strip())
        for stock in stocks:
            if mt.lower().find(stock.lower()) != -1:
                print(stock)
                print(mt.find(stock.lower()))
                SlotSet("symbol",stock.upper())
        message.text = mt

    @classmethod
    def load(
        cls,
        meta: Dict[Text, Any],
        model_dir: Optional[Text] = None,
        model_metadata: Optional["Metadata"] = None,
        cached_component: Optional["Component"] = None,
        **kwargs: Any
    ) -> "Component":
        if cached_component:
            return cached_component
        else:
            return cls(meta)