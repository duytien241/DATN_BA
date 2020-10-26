from rasa.nlu.components import Component
from rasa.nlu.training_data import Message
import typing
from typing import Any, Optional, Text, Dict

if typing.TYPE_CHECKING:
    from rasa.nlu.model import Metadata


class SpellCorrection(Component):

    provides = ["text"]
    defaults = {}
    language_list = ["en"]

    def __init__(self, component_config=None):
        super(SpellCorrection, self).__init__(component_config)

    def process(self, message, **kwargs):
        mt = message.text
        str = mt.translate(mt.maketrans(
            '', '', '!\"#$%&\'()*+,.-:;<=>?@[\]^_`{|}~'))
        words = str.split(' ')

        print(mt)
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
