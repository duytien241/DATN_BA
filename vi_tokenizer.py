import re
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.nlu.training_data import Message

from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize
from utils.remove_word import remove_word
from predict import Predictor

predictor = Predictor()

class VietnameseTokenizer(Tokenizer):

    provides = [TOKENS_NAMES[attribute] for attribute in MESSAGE_ATTRIBUTES]

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        AEIOUYD_VN = list("áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệiíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ")

        text= message.get(attribute)
        arr = text.split(' ')
        count = 0
        for i in arr:
            for t in i:
                if t in AEIOUYD_VN:
                    count = count + 1
        if count/len(arr) < 0.2:
            text=predictor.predict(text)
            print(text)
        words = remove_word(word_tokenize(text))
        print(words)
        return self._convert_words_to_tokens(words, text)
