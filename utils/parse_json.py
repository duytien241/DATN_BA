import re
import time
import json


def json2Text(text, action="", type_action="", message_type="", info = {}):
    json_response = {
        "text": text,
        "action": action,
        "type": type_action,
        "sender": "server",
        "timestamp": str(time.time()),
        "message_type": message_type,
    }
    json_response = {**json_response, **info}

    return json.dumps(json_response)

def json2Text_action( action="", type_action="", message_type="", info = {}):
    json_response = {
        "action": action,
        "type": type_action,
        "sender": "server",
        "timestamp": str(time.time()),
        "message_type": message_type,
    }
    json_response = {**json_response, **info}

    return json.dumps(json_response)