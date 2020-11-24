import json
from threading import Timer
import websocket
from typing import Any, Union
import logging

logging.basicConfig(
    format='%(asctime)s,%(msecs)d [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S')

import msgpack

from .Emitter import emitter
from .Parser import parse


class BlankDict(dict):
    def __missing__(self, key):
        return ""


def msgpackEncode(obj: Any):
    encoded = msgpack.packb(obj, use_bin_type=True)
    # logging.warning("encoded: %s, %s, %s", type(encoded), [b for b in encoded], encoded)
    return encoded


def msgpackDecode(msg: bytes):
    decoded = msgpack.unpackb(msg, raw=False)
    return decoded


class Packer:
    def __init__(self, is_enable_codec: bool):
        self.is_enable_codec = is_enable_codec

    def marshal(self, v: Any) -> bytes:
        # logging.warning("marshal: %s", v)
        if not self.is_enable_codec:
            return json.dumps(v, sort_keys=True)

        if ("cid" in v) and ("data" in v) and ("event" in v):
            if "authToken" in v["data"]:
                newV = {"e": [v["event"], v["data"], v["cid"]]}
                return msgpackEncode(newV)

            if "channel" not in v["data"]:
                return msgpackEncode(v)

            newV = {}
            array = []
            if v["event"] == "#publish":
                array.append(v["data"]["channel"])
                if "data" in v["data"]:
                    array.append(v["data"]["data"])
                else:
                    array.append(None)
                if v["cid"] != 0:
                    array.append(v["cid"])
                newV["p"] = array
            else:
                array.append(v["event"])
                array.append(v["data"])
                if v["cid"] != 0:
                    array.append(v["cid"])
                newV["e"] = array
            return msgpackEncode(newV)

        elif ("rid" in v) and ("data" in v) and ("error" in v):
            newV = {"r": [v["rid"], v["error"], v["data"]]}
            return msgpackEncode(newV)

        else:
            return msgpackEncode(v)

    def unmarshal(self, msg: bytes) -> Union[dict, str]:
        v = {}
        if not self.is_enable_codec:
            v = json.loads(msg, object_hook=BlankDict)
        else:
            v = msgpackDecode(msg)

        if type(v) is str:
            return v

        ret = {}
        array = []
        if "r" in v:
            array = v["r"]
            if len(array) != 3:
                return ret
            ret["rid"] = array[0]
            ret["error"] = array[1]
            ret["data"] = array[2]
            return ret
        if "p" in v:
            array = v["p"]
            ret["event"] = "#publish"
        elif "e" in v:
            array = v["e"]
        else:
            return ret
        if len(array) < 2:
            return ret
        ret["data"] = {"channel": array[0], "data": array[1]}
        if len(array) == 3:
            ret["cid"] = array[2]
        # logging.warning("unmarshal: msg: %s, ret: %s, v: %s", msg, ret, v)
        return ret


class socket(emitter):
    def __init__(self, url):
        self.packer: Packer = Packer(True)
        self.id = ""
        self.cnt = 0
        self.authToken = None
        self.url = url
        self.acks = {}
        self.channels = []
        self.enablereconnection = False
        self.delay = 3
        self.ws = self.onConnected = self.onDisconnected = self.onConnectError = self.onSetAuthentication = self.OnAuthentication = None
        emitter.__init__(self)

    def enablelogger(self, enabled):
        pass

    def emitack(self, event, object, ack):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        emitobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(emitobject))
        self.acks[self.cnt] = [event, ack]

    def emit(self, event, object):
        emitobject = json.loads('{}')
        emitobject["event"] = event
        emitobject["data"] = object
        self.send(self.packer.marshal(emitobject))

    def subscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(subscribeobject))
        self.channels.append(channel)

    def sub(self, channel):
        self.send(
            "{\"event\":\"#subscribe\",\"data\":{\"channel\":\"" + channel + "\"},\"cid\":" + str(
                self.getandincrement()) + "}")

    def subscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#subscribe"
        object = json.loads('{}')
        object["channel"] = channel
        subscribeobject["data"] = object
        subscribeobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(subscribeobject))
        self.channels.append(channel)
        self.acks[self.cnt] = [channel, ack]

    def unsubscribe(self, channel):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(subscribeobject))
        self.channels.remove(channel)

    def unsubscribeack(self, channel, ack):
        subscribeobject = json.loads('{}')
        subscribeobject["event"] = "#unsubscribe"
        subscribeobject["data"] = channel
        subscribeobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(subscribeobject))
        self.channels.remove(channel)
        self.acks[self.cnt] = [channel, ack]

    def publish(self, channel, data):
        publishobject = json.loads('{}')
        publishobject["event"] = "#publish"
        object = json.loads('{}')
        object["channel"] = channel
        object["data"] = data
        publishobject["data"] = object
        publishobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(publishobject))

    def publishack(self, channel, data, ack):
        publishobject = json.loads('{}')
        publishobject["event"] = "#publish"
        object = json.loads('{}')
        object["channel"] = channel
        object["data"] = data
        publishobject["data"] = object
        publishobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(publishobject))
        self.acks[self.cnt] = [channel, ack]

    def getsubscribedchannels(self):
        return self.channels

    def subscribechannels(self):
        for x in self.channels:
            self.sub(x)

    def Ack(self, cid):
        ws = self.ws

        def MessageAck(error, data):
            ackobject = json.loads('{}')
            ackobject["error"] = error
            ackobject["data"] = data
            ackobject["rid"] = cid
            ws.send(self.packer.marshal(ackobject))

        return MessageAck



    def on_message(self, ws, message):
        if message == "":  # ping without codec
            self.ws.send("")  # received ping, sending pong back
            return

        mainobject = self.packer.unmarshal(message)
        # logging.warning("on_message mainobject: %s", mainobject)
        if mainobject == "#1":
            pong = self.packer.marshal("#2")
            self.send(pong)
            return

        dataobject = {}
        if "data" in mainobject:
            dataobject = mainobject["data"]
        rid = ""
        if "rid" in mainobject:
            rid = mainobject["rid"]
        cid = ""
        if "cid" in mainobject:
            cid = mainobject["cid"]
        event = ""
        if "event" in mainobject:
            event = mainobject["event"]
        msgType = parse(dataobject, rid, cid, event)
        if msgType == 1:
            self.subscribechannels()
            if self.OnAuthentication is not None:
                self.id = dataobject["id"]
                self.OnAuthentication(self, dataobject["isAuthenticated"])
        elif msgType == 2:
            # logging.warning("received msg on channel: %s", dataobject)
            self.execute(dataobject["channel"], dataobject["data"])
        elif msgType == 3:
            self.authToken = None
            # remove token event received
        elif msgType == 4:
            # set token event received"
            if self.onSetAuthentication is not None:
                self.onSetAuthentication(self, dataobject["token"])
        elif msgType == 5:
            # received data for event
            if self.haseventack(event):
                self.executeack(event, dataobject, self.Ack(cid))
            else:
                self.execute(event, dataobject)
        else:
            if rid in self.acks:
                tuple = self.acks[rid]
                if tuple is not None:
                    # Ack received for event
                    ack = tuple[1]
                    ack(tuple[0], mainobject["error"], mainobject["data"])
                else:
                    # Ack function not found for rid
                    pass

    def on_error(self, ws, error):
        if self.onConnectError is not None:
            self.onConnectError(self, error)
            # self.reconnect()

    def on_close(self, ws):
        if self.onDisconnected is not None:
            self.onDisconnected(self)
        if self.enablereconnection:
            self.reconnect()

    def getandincrement(self):
        self.cnt += 1
        return self.cnt

    def resetvalue(self):
        self.cnt = 0

    def on_open(self, ws):
        self.resetvalue()

        handshakeobject = json.loads('{}')
        handshakeobject["event"] = "#handshake"
        object = json.loads('{}')
        object["authToken"] = self.authToken
        handshakeobject["data"] = object
        handshakeobject["cid"] = self.getandincrement()
        self.send(self.packer.marshal(handshakeobject))

        if self.onConnected is not None:
            self.onConnected(self)

    def setAuthtoken(self, token):
        self.authToken = str(token)

    def getAuthtoken(self):
        return self.authToken

    def connect(self, sslopt=None, http_proxy_host=None, http_proxy_port=None):
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever(sslopt=sslopt, http_proxy_host=http_proxy_host, http_proxy_port=http_proxy_port)

    def setBasicListener(self, onConnected, onDisconnected, onConnectError):
        self.onConnected = onConnected
        self.onDisconnected = onDisconnected
        self.onConnectError = onConnectError

    def reconnect(self):
        Timer(self.delay, self.connect).start()

    def setdelay(self, delay):
        self.delay = delay

    def setreconnection(self, enable):
        self.enablereconnection = enable

    def setAuthenticationListener(self, onSetAuthentication, OnAuthentication):
        self.onSetAuthentication = onSetAuthentication
        self.OnAuthentication = OnAuthentication

    def disconnect(self):
        self.enablereconnection = False
        self.ws.close()

    def send(self, msg: bytes):
        if self.ws is not None:
            self.ws.send(msg, 0x2)
