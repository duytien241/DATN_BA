# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from django.db.models import Count
from typing import Dict, Text, Any, List, Union, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, UserUtteranceReverted, Restarted
from rasa_sdk.executor import CollectingDispatcher
import random
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
import os
import sys
import json
import django
from datetime import datetime
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from app.models import Address, TimeOpen, Restaurant, MenuItem, Order, OrderDetail, District, User
from utils.common import getTimeOpenInTradeMark, checkInOneTradeMark, getLocationOfShop, getMenuOfRestaurant, getShopWithInfo, getShopWithLocation, getYNShopTime, calculateFeeShip, getTimeOfShop,get_cosine, text_to_vector
from utils.parse_json import json2Text, json2Text_action
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
# from predict import Predictor
import collections

list_shop_name = []
with open('resources/shop_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        list_shop_name.append(line.lower().strip())
    f.close()

list_food_name = []
with open('resources/food_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        list_food_name.append(line.lower().strip())
    f.close()

list_trademark = []
with open('resources/trademark.txt', 'r', encoding='utf8') as f:
    for line in f:
        list_trademark.append(line.lower().strip())
    f.close()

# reverse_index = {}
# for sentense in range(len(list_shop_name)):
#     arr_word = list_shop_name[sentense].split(' ')
#     for word in arr_word:
#         if word in reverse_index:
#             reverse_index[word].append(sentense)
#         else:
#             reverse_index[word] = [sentense]

DATABASE = ["bún đậu mắm tôm",
            "bún đậu nước mắm",
            "bún cá",
            "bún hải sản",
            "cơm văn phòng",
            "cơm sườn",
            "xôi",
            "bún ốc",
            "mì vằn thắn",
            "hủ tiếu",
            "bún chả",
            "bún ngan",
            "ngan xào tỏi",
            "bún bò huế",
            "mì tôm hải sản",
            "bánh mì trứng xúc xích rắc thêm ít ngải cứu",
            "bánh mì trứng",
            "bánh mì xúc xích",
            "bánh mì pate"]


class ActionHello(Action):

    def name(self) -> Text:
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot('cust_name')
        if name is None:
            name = 'quý khách'
        else:
            name = name.title()
        response = "Kính chào {}, Food Assistant Bot có thể giúp gì cho {} ạ?".format(
            name, name)
        dispatcher.utter_message(text=response)
        # do not affect to history
        return []


class ActionGoodBye(Action):

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        response = "Tạm biệt quý khác. chúc quý khách vui vẻ"
        dispatcher.utter_message(text=response)
        # do not affect to history
        return []


class ActionShowFunc(Action):
    def name(self) -> Text:
        return 'action_show_func'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=json2Text("Tôi có thể giúp bạn gợi ý món ăn?",action="SHOW_LIST_OPTIONS" ,info={'arr_options':"Đặt hàng, Tìm kiếm quán ăn, Hỏi giá, Tra cứu giá ship"}))

        return []


class ActionRecommend(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = []
        for i in range(2):
            food_number = random.randrange(len(DATABASE))
            food.append(DATABASE[food_number])

        dispatcher.utter_message(
            text="Em nghĩ hôm nay anh chị có thể thử món '{}' hoặc bên cạnh đó cũng có thể là món '{}' ạ".format(food[0], food[1]))

        return []

class ActionsHasOneTradeMark(Action):
    def name(self) -> Text:
        return "action_has_one_trademark"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        trademark = tracker.get_slot("trademark")
        print(trademark)
        if str(shop_name).lower() in list_trademark or trademark is not None:
            return [SlotSet("has_in_one_trademark", "has"), SlotSet("trademark",trademark)]
        else:
            return [SlotSet("has_in_one_trademark", "not")]

class ActionsHasOneShop(Action):
    def name(self) -> Text:
        return "action_store_has_one_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message['intent'].get('name') == 'order_food':
            list_shop = get_shop_name(tracker, True)
        else:
            list_shop = get_shop_name(tracker)
        print(list_shop)
        if len(list_shop) == 0:
            tmp = []
            shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
                                    if x['entity'] == 'shop_name'), None)
            train_set = [shop_name_chat]
            with open('resources/shop_name.txt', 'r', encoding='utf8') as f:
                for line in f:
                    train_set.append(line.strip())
                f.close()
            values = []
            try:
                tfidf_vectorizer = TfidfVectorizer()
                tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  #finds the tfidf score with normalization\
                tmp_cos = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)[0][1:]
                values = np.array(tmp_cos)
                pass
            except:
                pass
            if len(values) > 0:
                index_min = np.argmax(values)
            else:
                values = [0]
                index_min = 0
            print(values[index_min])
            if train_set[index_min] is not None and values[index_min] > 0.6:
                recommendation = train_set[index_min]
                return [SlotSet("has_one_shop", "not"),SlotSet("recommendation", recommendation), SlotSet("shop_name", None), SlotSet("trademark", None), SlotSet("pre_query", None)]
            else:
                return [SlotSet("has_one_shop", "not"), SlotSet("shop_name", None), SlotSet("trademark", None), SlotSet("pre_query", None)]
        elif len(list_shop) == 1:
            shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
                                    if x['entity'] == 'shop_name'), None)
            if tracker.get_slot("has_one_shop") == "not" and tracker.get_slot("trademark") != None and shop_name_chat is None:
                shop_name_chat = tracker.get_slot("trademark")
            text1 = list_shop[0].restaurant.name
            text2 = shop_name_chat
            print(text1, text2)
            if text2 is None:
                text2 = text1
            if text1 is None:
                text1 = text2
            vector1 = text_to_vector(text1)
            vector2 = text_to_vector(text2)
            if shop_name_chat is not None:
                cosine = get_cosine(vector1, vector2)
            else:
                cosine = 1
            print("cosine",cosine)
            if cosine > 0.6:
                return [SlotSet("has_one_shop", "has"), SlotSet("shop_name", list_shop[0].restaurant.name),  SlotSet("pre_query", list_shop)]
            return [SlotSet("has_one_shop", "not"),SlotSet("pre_query", None)]
        else:

            inTrademark = True
            trademark = list_shop[0].restaurant.trademark
            for item in list_shop:
                if item.restaurant.trademark != trademark:
                    inTrademark = False
            if inTrademark:
                return [SlotSet("has_one_shop", "not"), SlotSet("shop_name", None), SlotSet("trademark", trademark.name), SlotSet("pre_query", list_shop)]
            return [SlotSet("has_one_shop", "not"), SlotSet("shop_name", None), SlotSet("trademark", None)]

class ActionGetTimeShop(Action):
    def name(self) -> Text:
        return "action_get_time_of_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
        #                   if x['entity'] == 'shop_name'), None)
        # shop_name_slot = tracker.get_slot("shop_name")
        shop_name = tracker.get_slot("shop_name")
        pre_query = tracker.get_slot("pre_query")
        has_in_one_trademark = tracker.get_slot("has_in_one_trademark")
        if pre_query is None:
            res = getTimeOfShop(shop_name)
            print("res", res, shop_name)
            if res is not None and len(res) == 1:
                item = res[0].time_open
                print(item.time_open)
                if item.has_two_shift:
                    dispatcher.utter_message(
                        text="Quán {} mở cửa từ {} tới {} và từ {} tới {} ạ."
                            .format(shop_name, 
                                item.shift_one_start, 
                                item.shift_one_end, 
                                item.shift_two_start, 
                                    item.shift_two_end, ))
                else:
                    dispatcher.utter_message(
                        text="Quán {} mở cửa từ {} tới {} ạ.".format(shop_name, item.shift_one_start, item.shift_one_end))
            else:
                dispatcher.utter_message(
                    text="Không có kết quả nào phù hợp. Bạn vui lòng kiểm tra lại tin nhắn")
            return [SlotSet("has_one_shop", "not"), ]
        if len(pre_query) == 1:
            item = pre_query[0]['restaurant']['time_open']
            if item['has_two_shift']:
                dispatcher.utter_message(
                    text="Quán {} mở cửa từ {} tới {} và từ {} tới {} ạ."
                        .format(shop_name, 
                            item['shift_one_start'], 
                            item['shift_one_end'], 
                            item['shift_two_start'], 
                            item['shift_two_end'], ))
            else:
                dispatcher.utter_message(
                    text="Quán {} mở cửa từ {} tới {} ạ.".format(shop_name, item['shift_one_start'], item['shift_one_end']))
            return [SlotSet("has_one_shop", "has")]
        elif len(pre_query) == 0:
            dispatcher.utter_message(
                text="Quán {} không tồn tại. Bạn vui lòng kiểm tra lại nhé!".format(shop_name))
            return [SlotSet("has_one_shop", "not")]
        elif has_in_one_trademark:
            message = 'Quán {} có các cơ sở với thời gian mở cửa sau:\n'.format(pre_query[0]['restaurant']['trademark']['name'])
            res = getTimeOpenInTradeMark(pre_query, True)
            for item in res:
                item_json  = json.loads(item)
                if item_json['has_two_shift']:
                    message  = message + "Cơ sở {} mở cửa từ {} tới {} và từ {} tới {}.\n".format(', '.join(res[item]), 
                                                                                        item_json['shift_one_start'],
                                                                                        item_json['shift_one_end'],
                                                                                        item_json['shift_two_start'],
                                                                                        item_json['shift_two_end'])
                else:
                    message = message + "Các Cơ sở {} mở cửa từ {} tới {}.\n".format(', '.join(res[item]), item_json['shift_one_start'],item_json['shift_one_end'],)
            dispatcher.utter_message(text=message)
            return [SlotSet("has_one_shop", "not"),SlotSet("email", "not")]
            # dispatcher.utter_message(
            #     text="Bạn muốn hỏi cơ sở nào nhỉ:\n" + "\n".join(i.name for i in shop_arr))
        else:
            dispatcher.utter_message(
                text="Có khá nhiều cửa hàng với từ khóa mà bạn tìm kiếm.Bạn vui lòng kiểm tra lại nhé.")
            return [SlotSet("has_one_shop", "not")]


class ActionGetLocationShop(Action):
    def name(self) -> Text:
        return "action_get_location_of_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        trademark_slot = tracker.get_slot("trademark")
        pre_query = tracker.get_slot("pre_query")
        location = next((x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        if shop_name is not None:
            list_location = getLocationOfShop(shop_name,location)
        else:
            list_location = getLocationOfShop(trademark_slot,location)
        if len(list_location) == 1 and location is not None:
            dispatcher.utter_message(
                text="Địa chỉ quán tại {} là: {} ạ.\nChúc anh/chị có bữa ăn ngon miệng ^^.".format(location, list_location[0].address_full))
            return [SlotSet("shop_name",list_location[0].restaurant.name)]
        elif location is None and len(list_location) == 1:
            dispatcher.utter_message(
                text="Địa chỉ quán là: {} ạ.\nChúc anh/chị có bữa ăn ngon miệng ^^.".format(list_location[0].address_full))
        elif len(list_location) > 1:
            dispatcher.utter_message(
                text="Có quá nhiều kết quả khớp. Vui lòng kiểm tra lại tên quán nhé bạn")
        else:
            dispatcher.utter_message(text="Không có kết quả phù hợp. Vui lòng kiểm tra lại tên quán nhé bạn")
        return []


class ActionGetFoodTypeInLocation(Action):
    def name(self) -> Text:
        return "action_get_food_type_in_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        food_type = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'food_type'), None)
        location = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        if food_type is not None and location is not None:
            result = Restaurant.objects.filter(name__contains = food_type)
            if(result is not None):
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" + "\n".join("Tên quán: "+name.name + " địa chỉ: "+str(name.rating)+","+name.cost for name in result))
            else:
                dispatcher.utter_message(text="Không tìm thấy quán")

        else:
            dispatcher.utter_message(
                text="Không tìm thấy quán")

        return []


class ActionGetFoodInfo(Action):
    def name(self) -> Text:
        return "action_get_food_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="trà sữa toco")

        return []

class ActionGetFoodPrice1(Action):
    def name(self) -> Text:
        return "action_get_food_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="Giá của  {} là: ")
        else:
            dispatcher.utter_message(
                text="Giá của  {} là: ")

        return []


class ActionGetYesNoFoodInfoLocation(Action):
    def name(self) -> Text:
        return "action_yes_no_food_info_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'food_name'), None)
        location = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        if food_name is not None and location is not None:
            result = []
            print(result)
            if(result is not None):
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" + "\n".join("Tên quán: "+name[0] + " địa chỉ: "+name[1]+","+name[2] for name in result))
            else:
                dispatcher.utter_message(text="Không tìm thấy quán")

        else:
            dispatcher.utter_message(
                text="Không tìm thấy quán")

        return []


class ActionYesNoShopTypeWithPrice(Action):
    def name(self) -> Text:
        return "action_yes_no_shop_type_with_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="ko có cửa hàng với mức giá")
        else:
            dispatcher.utter_message(
                text="có cửa hàng với mức giá")

        return []


class ActionYesNoTrademarkLocation(Action):
    def name(self) -> Text:
        return "action_yes_no_trademark_with_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="ko có thương hiệu")
        else:
            dispatcher.utter_message(
                text="có thương hiệu")

        return []


class ActionShowNumberOfTrademark(Action):
    def name(self) -> Text:
        return "action_number_trademark_with_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="thương hiệu")
        else:
            dispatcher.utter_message(
                text="số lượng thương hiệu")

        return []


class ActionShowShopInLocation(Action):
    def name(self) -> Text:
        return "action_show_shop_in_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shop_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'shop_name'), None)
        location = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        if shop_name is not None and location is not None:
            result = []
            if result is not None:
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" + "\n".join("Tên quán: "+name[0] + " địa chỉ: "+name[1]+","+name[2] for name in result))
            else:
                dispatcher.utter_message(text="Không tìm thấy")

        else:
            dispatcher.utter_message(
                text="Vui lòng nhập lại thông tin")

        return []


class ActionShowFeeShip(Action):
    def name(self) -> Text:
        return "action_show_fee_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="Quán ko thấy sip")
        else:
            dispatcher.utter_message(
                text="Quán {} có phí ship khoảng")

        return []


class ActionShowShopShip(Action):
    def name(self) -> Text:
        return "action_show_avg_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="""Với khoảng các dưới 3km thì phí vận chuyển là 15000 đồng, với đơn xa hơn thì giá là 25,000 đồng.
                    \nVới đơn hàng xa hơn 10km thì shop không hỗ trợ vận chuyển ạ""")
        return []


class ActionShowAvgShip(Action):
    def name(self) -> Text:
        return "action_show_shop_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        location = tracker.get_slot("location")
        fee_ship = calculateFeeShip(location, shop_name)
        if fee_ship is None:         
            dispatcher.utter_message(
                text="Quán không hỗ trợ ship đến địa chỉ của bạn ạ. Rất xin lỗi bạn vì sự bất tiện này.")
        else:
            dispatcher.utter_message(
                text="Phí ship của quán {} tới địa chỉ {} là {}.".format(shop_name, location, fee_ship))

        return []


class ActionShowFreeShip(Action):
    def name(self) -> Text:
        return "action_show_free_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="""Với khoảng các dưới 3km thì phí vận chuyển là 15000 đồng, với đơn xa hơn thì giá là 25,000 đồng.
                    \nVới đơn hàng xa hơn 10km thì shop không hỗ trợ vận chuyển ạ""")

        return []


class ActionStoreShopName(Action):
    def name(self) -> Text:
        return "action_store_shop_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shop_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'shop_name'), None)
        return [SlotSet("shop_name", shop_name)]


class ActionStoreHasShopName(Action):
    def name(self) -> Text:
        return "action_store_has_shop_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shop_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'shop_name'), None)
        shop_arr = []
        if len(shop_arr) == 1:
            return [SlotSet("has_shop_name", "has")]
        elif len(shop_arr) == 0:
            return [SlotSet("has_shop_name", "not")]
        else:
            return [SlotSet("has_shop_name", "not")]


class ActionStoreFoodName(Action):
    def name(self) -> Text:
        return "action_store_food_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'food_name'), None)
        return [SlotSet("shop_name", food_name)]


class ActionStoreFoodType(Action):
    def name(self) -> Text:
        return "action_store_food_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_type = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'food_type'), None)
        return [SlotSet("food_type", food_type)]


class ActionStoreHasFoodType(Action):
    def name(self) -> Text:
        return "action_store_has_food_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_type = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'food_type'), None)
        if food_type is not None:
            return [SlotSet("has_food_type", "has")]
        else:
            return [SlotSet("has_food_type", "not")]


class ActionStoreTradeMark(Action):
    def name(self) -> Text:
        return "action_store_trademark"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        trademark = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'trademark'), None)
        return [SlotSet("trademark", trademark)]

class ActionStorePrice(Action):
    def name(self) -> Text:
        return "action_store_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        price = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'price'), None)
        return [SlotSet("price", price)]


class ActionStoreTime(Action):
    def name(self) -> Text:
        return "action_store_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        list_time = []
        for x in tracker.latest_message['entities']:
            if x['entity'] == 'time':
                time = str(x["value"])
                time = time.replace("buổi","").replace("và","").strip()
                if time not in list_time and len(time) != 0:
                    list_time.append(time)
        return [SlotSet("time", list_time)]


class ActionStoreEmail(Action):
    def name(self) -> Text:
        return "action_store_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        email = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'email'), None)
        return [SlotSet("email", email)]


class ActionStorePhone(Action):
    def name(self) -> Text:
        return "action_store_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        phone = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'phone'), None)
        return [SlotSet("phone", phone)]


class ActionStoreFullName(Action):
    def name(self) -> Text:
        return "action_store_full_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        full_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'full_name'), None)
        return [SlotSet("full_name", full_name)]


class ActionStoreCustName(Action):
    def name(self) -> Text:
        return "action_store_cust_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cust_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'cust_name'), None)
        return [SlotSet("cust_name", cust_name)]


class ActionYNTime(Action):

    def name(self) -> Text:
        return "action_yes_no_shop_with_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'shop_name'), None)
        shop_name_slot = tracker.get_slot("shop_name")
        trademark_slot = tracker.get_slot("trademark")
        pre_query = tracker.get_slot("pre_query")
        shop_name = shop_name_chat if shop_name_chat is not None else shop_name_slot
        list_time = tracker.get_slot("time")
        # time = next(
        #     (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'time'), None)
        if shop_name_slot is None and trademark_slot is None:
            dispatcher.utter_message(
                text="Quán {} không tồn tại trong cơ sở dữ liệu của chúng tôi! Xin lỗi vì sự bất tiện này.".format(shop_name_chat))
        elif shop_name is not None:
            message = getYNShopTime(shop_name, list_time, True, pre_query)
            dispatcher.utter_message(text=message)
        return []


class ActionGetShopWithType(Action):

    def name(self) -> Text:
        return "action_show_list_shop_match"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'food_type'), None)
        food_type_slot = tracker.get_slot("food_type")
        food_type = food_type_chat if food_type_chat is not None else food_type_slot
        shop_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'shop_type'), None)
        shop_type_slot = tracker.get_slot("shop_type")
        shop_type = shop_type_chat if shop_type_chat is not None else shop_type_slot
        time = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'cust_name'), None)
        if shop_type is None:
            time_arr = []
            print(time_arr)
            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q='" +
                tracker.latest_message['text'].replace(" ", "%20") + "'")
        return []


class ActionShowInfoOrder(Action):

    def name(self) -> Text:
        return "action_show_order_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'food_type'), None)
        food_type_slot = tracker.get_slot("food_type")
        food_type = food_type_chat if food_type_chat is not None else food_type_slot
        shop_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'shop_type'), None)
        shop_type_slot = tracker.get_slot("shop_type")
        shop_type = shop_type_chat if shop_type_chat is not None else shop_type_slot
        time = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'cust_name'), None)
        dispatcher.utter_message(
            text="Thông tin đặt hàng của bạn là: https://www.google.com.vn/search?q='" +
            tracker.latest_message['text'].replace(" ", "%20") + "'")
        return []


class ActionAskShop(Action):

    def name(self) -> Text:
        return "action_ask_shop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        has_in_one_trademark = tracker.get_slot("has_in_one_trademark")
        pre_query = tracker.get_slot("pre_query")
        recommendation = tracker.get_slot("recommendation")
        if pre_query is not None and has_in_one_trademark == 'has':
            if tracker.get_latest_input_channel() == "socketcluster":
                mess = ''
                for item in pre_query:
                    arr_name = str(item["restaurant"]["name"]).split('-')
                    mess = mess + arr_name[-1] + ','
                dispatcher.utter_message("Bạn muốn hỏi cửa hàng nào. Quán có các cơ sở sau:")
                dispatcher.utter_message(text=json2Text_action(action="SHOW_LIST_OPTIONS", info={'arr_options':mess}))
            else:
                mess = ''
                for item in pre_query:
                    arr_name = str(item["restaurant"]["name"]).split('-')
                    mess = mess +'\n-' + arr_name[-1]
                dispatcher.utter_message("Bạn muốn hỏi cửa hàng nào. Quán có các cơ sở sau:" +mess)
        elif recommendation is not None:
            dispatcher.utter_message(
                text="Bạn muốn hỏi cửa hàng nào nhỉ. Có phải bạn muốn hỏi quán: {}".format(recommendation))
            dispatcher.utter_message(text=json2Text_action(action="SHOW_LIST_OPTIONS", info={'arr_options':'Đúng vậy, Không phải'}))
        else:
            dispatcher.utter_message(
                text="Bạn muốn hỏi cửa hàng nào nhỉ.")
        return []


class ActionYesRecommendation(Action):

    def name(self) -> Text:
        return "action_replace_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recommendation = tracker.get_slot("recommendation")
        return [SlotSet("shop_name", recommendation)]

class ActionChooseShop(Action):

    def name(self) -> Text:
        return "action_choosen_shop "

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'food_type'), None)
        has_in_one_trademark = tracker.get_slot("has_in_one_trademark")
        shop_type_chat = next((x["value"] for x in tracker.latest_message['entities']
                               if x['entity'] == 'shop_type'), None)
        pre_query = tracker.get_slot("pre_query")
        if pre_query is not None and has_in_one_trademark == 'has':
            mess = ''
            for item in pre_query:
                arr_name = str(item["restaurant"]["name"]).split('-')
                mess = mess +'\n- ' + arr_name[-1]
            dispatcher.utter_message("Bạn muốn hỏi cửa hàng nào. Quán có các cơ sở sau:" +mess)
        else:
            dispatcher.utter_message(
                text="Bạn muốn hỏi cửa hàng nào nhỉ")
        return []


class ActionSaveInfoOrder(Action):

    def name(self) -> Text:
        return "action_save_info_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cart_food = []
        cart_quantity = []
        last_index = 0
        current_index = 0
        for x in tracker.latest_message['entities']:
            if x['entity'] == 'food_name' and x['entity'] not in cart_food and x['extractor'] == 'CRFEntityExtractor':
                current_index = x["start"]
                
                cart_food.append(x["value"])
            if x['entity'] == 'number' and x['entity'] not in cart_food and x['extractor'] == 'CRFEntityExtractor':
                cart_quantity.append(x["value"])
        print("cart_food", cart_food)
        print("cart_quantity", cart_quantity)
        return [SlotSet("cart_food",cart_food if len(cart_food) != 0 else None ), SlotSet("cart_quantity",cart_quantity if len(cart_quantity) != 0 else None )]

class OrderFormInfo(FormAction):

    list_food = []

    def name(self) -> Text:

        return "order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["userId", "shop_name", "cart_food", "cart_quantity", "cust_name", "address", "phone", "note", "is_confirm"]

    def request_next_slot(self,
                          dispatcher,  # type: CollectingDispatcher
                          tracker,  # type: Tracker
                          domain  # type: Dict[Text, Any]
                          ):
        # type: (...) -> Optional[List[Dict]]
        """Request the next slot and utter template if needed,
            else return None"""

        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            dispatcher.utter_message(
                text="Vâng ạ! Rất mong lần sau tiếp tục được phục vụ quý khách!")
            return self.deactivate()
        else:
            for slot in self.required_slots(tracker):
                if self._should_request_slot(tracker, slot):
                    if slot == "userId":
                        dispatcher.utter_message(
                            text=json2Text_action("LOG_IN"))
                    elif slot == "shop_name":
                        dispatcher.utter_message(
                            text="Vui lòng cung cấp quán bạn muốn đặt")
                    elif slot =="cart_food":
                        shop_name = tracker.get_slot("shop_name")
                        menu = MenuItem.objects.filter(restaurant__name = shop_name)
                        menu_arr = []
                        print("cart_food1",tracker.get_slot("cart_food"))
                        if menu is not None:
                            for x in menu:
                                if x is not None:
                                    menu_arr.append(x.name)
                        dispatcher.utter_message(
                            text="Bạn muốn đặt món nào. Quán có 1 số món sau đây:" + ",".join(menu_arr) )
                    elif slot =="cart_quantity":
                        print(tracker.get_slot("shop_name"))
                        print("cart_quantity",tracker.get_slot("cart_quantity"))
                        print("cart_food",tracker.get_slot("cart_food"))
                        dispatcher.utter_message(
                            text="Vui lòng cung cấp số lượng bạn muốn đặt")
                    elif slot =="cust_name":
                        dispatcher.utter_message(
                            text="Tên của bạn là?")
                    elif slot =="address":
                        dispatcher.utter_message(
                            text="Địa chỉ nhận hàng của bạn?")
                    elif slot =="phone":
                        dispatcher.utter_message(
                            text="Số điện thoại để shipper tiện liên lạc nhá.")
                    elif slot =="note":
                        dispatcher.utter_message(
                            text="Bạn muốn ghi chú gì không.")
                    elif slot == "is_confirm":
                        mess="""{} đã đặt hàng với ghi chú là {}.\n
                                Đơn hàng của bạn sẽ được giao tới địa chỉ {} 
                                với số điện thoại là {}. Chi tiết đơn hàng là:\n""".format(tracker.get_slot("cust_name"),
                                                                                            tracker.get_slot("note"),
                                                                                            tracker.get_slot("address"),
                                                                                            tracker.get_slot("phone"))
                        for idx, val in enumerate( tracker.get_slot("cart_quantity")):
                            mess = mess + "{} phần {}".format(val, tracker.get_slot("cart_food")[idx])
                        dispatcher.utter_message(
                            text=mess)
                        dispatcher.utter_message(
                            text="Bạn xác nhận đặt hàng chứ.")
                    return [SlotSet(REQUESTED_SLOT, slot)]
            return None

    def validate_shop_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"shop_name": None}
        list_shop = get_shop_name(tracker)
        print(list_shop)
        if len(list_shop) == 0:
            tmp = []
            shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
                                    if x['entity'] == 'shop_name'), None)
            train_set = [shop_name_chat]
            with open('resources/shop_name.txt', 'r', encoding='utf8') as f:
                for line in f:
                    train_set.append(line.strip())
                f.close()
            values = []
            try:
                tfidf_vectorizer = TfidfVectorizer()
                tfidf_matrix_train = tfidf_vectorizer.fit_transform(train_set)  #finds the tfidf score with normalization\
                tmp_cos = cosine_similarity(tfidf_matrix_train[0:1], tfidf_matrix_train)[0][1:]
                values = np.array(tmp_cos)
                pass
            except:
                pass
            index_min = np.argmax(values)
            if train_set[index_min] is not None:
                recommendation = train_set[index_min]
                dispatcher.utter_message(
                    text="Tên quán không tồn tại. Vui lòng kiểm tra và nhập lại. Có phải bạn muốn hỏi quán {}".format(recommendation))
                return {"shop_name": None}
            else:
                dispatcher.utter_message(
                    text="Tên quán không tồn tại. Vui lòng kiểm tra và nhập lại.")
        elif len(list_shop) == 1:
            shop_name = list_shop[0].restaurant.name
            menu = getMenuOfRestaurant(shop_name)
            if len(menu) == 0:
                dispatcher.utter_message(
                    text="Các món của quán {} đang được cập nhật. Bạn vui lòng đặt hàng ở quán khác nhé.".format(shop_name))
                return {"shop_name": None}
            else:
                return {"shop_name": list_shop[0].restaurant.name, "menu": menu}
        else:
            inTrademark = True
            trademark = list_shop[0].restaurant.trademark
            for item in list_shop:
                if item.restaurant.trademark != trademark:
                    inTrademark = False
            if inTrademark:
                dispatcher.utter_message(
                    text="Tên quán không tồn tại. Vui lòng kiểm tra và nhập lại")
            dispatcher.utter_message(
                    text="Tên quán không tồn tại. Vui lòng kiểm tra và nhập lại")

    def validate_cart_food(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"food_name": None}
        shop_name = tracker.get_slot("shop_name")
        cart_food = tracker.get_slot("cart_food")
        menu = MenuItem.objects.filter(restaurant__name=shop_name)
        food_name = next((x["value"] for x in tracker.latest_message['entities']
                    if x['entity'] == 'food_name'), None)
        number = next((x["value"] for x in tracker.latest_message['entities']
                    if x['entity'] == 'number'), None)
        if number is None:
            number = []
        else:
            number = [number]
        cart_food = None
        if tracker.get_slot("cart_food") is not None:
            cart_food = tracker.get_slot("cart_food")
        if food_name and str(food_name).lower() in list_food_name:
            cart_food = []
            cart_food.append(food_name)
            return {"cart_food": cart_food, "cart_quantity": number}
        elif food_name is not None :
            dispatcher.utter_message(
                text="Tên món ăn không có trong quán. Bạn có thể xem các món: " + ", ".join(item.name for item in menu) )
            return {"cart_food": cart_food}
        return {"cart_food": cart_food, "cart_quantity": number}

    def validate_cart_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"food_name": None}
        quantity_order = next((x["value"] for x in tracker.latest_message['entities']
                    if x['entity'] == 'number'), None)
        cart_quantity = None
        if tracker.get_slot("cart_quantity") is not None:
            cart_quantity = tracker.get_slot("cart_quantity")
        print("cart_quantitycart_quantity",cart_quantity)
        if quantity_order in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            cart_quantity = []
            cart_quantity.append(quantity_order)
            return {"cart_quantity": cart_quantity}
        elif cart_quantity is not None:
            return {"cart_quantity": cart_quantity}
        else:
            dispatcher.utter_message(
                text="Vui lòng cung cấp chính xác số lượng đặt." )
            return {"cart_quantity": None}

    def validate_address(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"address": None}
        location = next((x["value"] for x in tracker.latest_message['entities']
                    if x['entity'] == 'location'), None)
        print((location, tracker.get_slot("shop_name")))
        feeship = calculateFeeShip(location, tracker.get_slot("shop_name"))
        if feeship == 0:
            dispatcher.utter_message(
                text="Địa chỉ không hợp lệ. Vui lòng nhập lại")
            return {"address": None}
        else:
            dispatcher.utter_message(
                text="Với địa chỉ được giao phí ship sẽ là {}".format(feeship))
            return {"address": location}

    def validate_note(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"note": None}
        return {"note": value}

    def validate_userId(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"note": None}
        number = next((x["value"] for x in tracker.latest_message['entities']
                    if x['entity'] == 'number'), None)
        print(number)
        if number:
            return {"userId": number}
        return {"userId": None}

    def validate_phone(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        phone = re.search("(84|\+84}{|0)\d{9,10}", value)
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung cấp được bảo mật tuyệt đối ạ!")
            return {"phone": None}
        print(phone)
        if not phone:
            dispatcher.utter_message(
                text="Số điện thoại không hợp lệ! Mời quý khách kiểm tra lại.")
            return {"phone": None}
        else:
            phone = phone.group()
            return {"phone": phone}

    def validate_is_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung cấp được bảo mật tuyệt đối ạ!")
            return {"phone": None}
        if not tracker.latest_message['intent']['name'] == "affirm":
            dispatcher.utter_message(
                text="Nhập đồng ý để xác nhận đặt hàng.")
            return {"is_confirm": None}
        else:
            return {"is_confirm": "yes"}

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "shop_name": self.from_text(),
            "cart_food": self.from_text(),
            "cart_quantity": self.from_text(),
            "cust_name": self.from_text(),
            "address": self.from_text(),
            "phone": self.from_text(),
            "note": self.from_text(),
            "is_confirm": self.from_text(),
            "userId": self.from_text(),
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        print(tracker.get_slot("cart_food"))
        menu_item = MenuItem.objects.filter(name__icontains=tracker.get_slot("cart_food")[0], restaurant__name__icontains = tracker.get_slot("shop_name"))
        if(len(menu_item)> 0):
            menu_item = menu_item[0]
        order = Order()
        print(tracker.get_slot("shop_name"))
        order.address_ship = tracker.get_slot("address")
        order.phone = tracker.get_slot("phone")
        order.note = tracker.get_slot("note")
        order.restaurant = Restaurant.objects.filter(name__icontains=tracker.get_slot("shop_name"))[0]
        order.status = 'Chưa giao hàng'
        order.time_order = datetime.today()
        order.user = User.objects.get(pk=tracker.get_slot("userId"))
        order.total_cost = int(menu_item.price.replace(",","").replace("đ","")) * int(tracker.get_slot("cart_quantity")[0])
        order.save()
        orderDetail = OrderDetail()
        orderDetail.order = order;
        print(tracker.get_slot("cart_quantity"),tracker.get_slot("cart_food") )
        orderDetail.menu_item = menu_item
        orderDetail.quantity = tracker.get_slot("cart_quantity")[0]
        orderDetail.save()
        if menu_item is None:
            dispatcher.utter_message(
                text="Bot đã lưu lại thông tin đặt đơn hàng của bạn. Đơn sẽ sớm được giao tới bạn. Chúc bạn ngon miệng nhé ^^.")
        else:
            dispatcher.utter_message(
                text="Bot đã lưu lại thông tin đặt đơn hàng của bạn. Đơn sẽ sớm được giao tới bạn. Chúc bạn ngon miệng nhé ^^.")
        return []

class act_unknown(Action):

    def name(self) -> Text:
        return "act_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Vui lòng nhập lại tin nhắn")
        return []

class ActionGetMenuShop(Action):

    def name(self) -> Text:
        return "action_get_menu_shop"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        print(shop_name)
        menu = getMenuOfRestaurant(shop_name)
        if (menu is None or len(menu) == 0) and shop_name is not None:
            dispatcher.utter_message(
                text="Menu của quá {} chưa được cập nhật".format(shop_name))
        elif len(menu) != 0 and shop_name is not None:
            dispatcher.utter_message(
                text="Quán {} có các món sau đây:\n{}".format(shop_name, "\n".join(item.name for item in menu )))
        return []

class ActionAskLocation(Action):

    def name(self) -> Text:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_latest_input_channel())
        dispatcher.utter_message(
                text="Bạn có thể cung cấp địa chỉ hiện tại của bạn để chúng tôi tìm dễ hơn không.")
        if tracker.get_latest_input_channel() == "socketcluster":
            dispatcher.utter_message(text=json2Text_action("GET_ADDRESS"))
        return []

class ActionsHasLocation(Action):
    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'location'), None)
        print(location)
        if location is not None:
            if location in ["gần đây", "đây", "này"] and tracker.get_slot("current_address") is None:
                return [SlotSet("has_location", "has"),SlotSet("is_near", "has"), SlotSet("location", location), SlotSet("has_address","not")]
            else:
                if location in ["gần đây", "đây", "này"]:
                    return [SlotSet("has_location", "has"), SlotSet("location", tracker.get_slot("current_address")), SlotSet("is_near", "not"), SlotSet("has_address","has")]
                elif tracker.get_slot("is_near") == "has":
                    return [SlotSet("has_location", "has"), SlotSet("location", location), SlotSet("is_near", "not"), SlotSet("current_address", location), SlotSet("has_address","has")]
                else:
                    return [SlotSet("has_location", "has"), SlotSet("location", location), SlotSet("is_near", "not"), SlotSet("has_address","has")]
        else:
            return [SlotSet("has_location", "not"), SlotSet("location", None), SlotSet("is_near", "not"), SlotSet("has_address","not")]

class ActionGetShopWithInfo(Action):
    def name(self) -> Text:
        return "action_get_shop_in_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        res = getShopWithInfo(location = tracker.get_slot("location"), shop_type= tracker.get_slot("shop_type"), time=tracker.get_slot("time") )
        if(len(res) == 0):
            dispatcher.utter_message(text="Xin lỗi! Rất tiếc vì không tìm thấy cửa hàng nào theo yêu cầu của bạn.")
        else:
            arr = []
            message = 'Có các quán sau đây:\n'
            i = 0
            for item in res:
                arr.append(str(res[item].restaurant.id))
                i = i + 1
                if i < 6:
                    message = message + "- {} địa chỉ: {}\n".format(res[item].restaurant.name, res[item].address_full)
                
            dispatcher.utter_message(text=message)
            if tracker.get_latest_input_channel() == "socketcluster":
                print(arr)
                dispatcher.utter_message(text=json2Text_action("SAVE_SEARCH", info={'arr_options':  ",".join(arr) }))
        return []

class ActionGetFoodPrice(Action):
    def name(self) -> Text:
        return "action_get_food_price"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        food_name = tracker.get_slot("food_name")
        print(shop_name, food_name)
        if food_name is not None and shop_name is not None:
            food = MenuItem.objects.filter(restaurant__name__icontains = shop_name, name__icontains=food_name)
        elif food_name is None:
            food = MenuItem.objects.filter(restaurant__name__icontains = shop_name)
        else:
            food = []
        print(food)
        if len(food) == 1:
            dispatcher.utter_message(
                    text="Giá của món {} là: {}".format(food_name,food[0].price))
        else:
            dispatcher.utter_message(
                    text="Vui lòng kiểm tra lại, món {} không tồn tại.".format(food_name))
        return []

class ActionStoreFoodName(Action):
    def name(self) -> Text:
        return "action_store_has_food_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        has_one_shop = tracker.get_slot("has_one_shop")
        has_in_one_trademark = tracker.get_slot("has_in_one_trademark")
        food_name = next((x["value"] for x in tracker.latest_message['entities']
                        if x['entity'] == 'food_name'), None)
        print(food_name, tracker.get_slot("trademark"),shop_name)
        if shop_name is None:
            shop_name = tracker.get_slot("trademark")
        if has_one_shop == "not":
            return [SlotSet("has_food_name","not"), SlotSet("food_name",food_name)]
        else:
            if food_name is None:
                return [SlotSet("has_food_name","not"), SlotSet("food_name",None)]
            else:
                res = []
                if has_in_one_trademark == "has" and has_one_shop == "not":
                    res = MenuItem.objects.filter(restaurant__name__icontains=shop_name, name__icontains = food_name).values_list('name','price').distinct()
                elif has_one_shop == "has":
                    res = MenuItem.objects.filter(restaurant__name=shop_name, name__icontains = food_name)
                if len(res) == 1:
                    return [SlotSet("has_food_name","has"), SlotSet("food_name",res[0].name)]
                else:
                    return [SlotSet("has_food_name","not"), SlotSet("food_name",food_name)]
        return [SlotSet("has_food_name","not"), SlotSet("food_name",food_name)]

class ActionAskInfo(Action):
    def name(self) -> Text:
        return "ation_ask_information_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        has_one_shop =tracker.get_slot("has_one_shop") 
        if has_one_shop == "has":
            res = Restaurant.objects.get(name = shop_name)
            if len(res.phone) == 0:
                dispatcher.utter_message(
                        text="Số điện thoại của quán chưa được cập nhật")
            else:
                phone = res.phone
                dispatcher.utter_message(
                        text="Số điện thoại của quán là: {}".format(phone))
        return []


class ActionGetOption(Action):
    def name(self) -> Text:
        return "action_get_option_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        has_one_shop =tracker.get_slot("has_one_shop") 
        dispatcher.utter_message(
                        text="Quán có wifi, chỗ để xe máy còn chỗ để ô tô bạn vui lòng gửi ở bãi xe gần nhất nhé.")
        return []


class ActionStoreShopType(Action):
    def name(self) -> Text:
        return "action_store_shop_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_type = next((x["value"] for x in tracker.latest_message['entities']
                        if x['entity'] == 'shop_type'), None)
        return [SlotSet("shop_type",shop_type)]

class ActionAskLocation(Action):
    def name(self) -> Text:
        return "action_ask_for_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                        text="Với địa chỉ này bạn muốn hỏi gì nhể")
        return []


def get_shop_name(tracker, without_food_name = False):
    shop_name_slot = tracker.get_slot("shop_name")
    shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
    shop_name = shop_name_chat if shop_name_chat is not None else shop_name_slot
    location = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'location'), None)
    if tracker.get_slot("has_one_shop") == "not" and tracker.get_slot("trademark") != None and shop_name is None:
        shop_name = tracker.get_slot("trademark")
    if shop_name is None and without_food_name == False:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                      if x['entity'] == 'food_name'), None)
    print(shop_name)
    return getShopWithLocation(shop_name, location)

class ActionDeny(Action):
    def name(self) -> Text:
        return "ation_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                        text="Bạn muốn hỏi thông tin gì khác nhỉ?")
        return []
        
class ActionStoreDeny(Action):
    def name(self) -> Text:
        return "action_store_deny"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("has_deny", "has")]

class ActionCheckOrder(Action):
    def name(self) -> Text:
        return "action_get_status_order"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        order = Order.objects.filter(user_id = tracker.get_slot("userId"), status__icontains ='Chưa giao hàng')
        print(order)
        if len(order) != 0:
            mess = ''
            for item in order:
                mess = mess + 'MS{} của nhà hàng {} với trạng thái {}\n'.format(item.id,item.restaurant.name, item.status)

            dispatcher.utter_message(
                            text="Bạn đang có những đơn hàng này được xử lý:\n{}".format(mess))
        else:
            dispatcher.utter_message(
                            text="Bạn đang không có đơn hàng nào.")
        return []

class ActionStoreAddres(Action):
    def name(self) -> Text:
        return "action_store_current_address"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'location'), None)
        return [SlotSet("current_address", "location")]

class ActionThanks(Action):
    def name(self) -> Text:
        return "action_thanks"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                        text="Cảm ơn bạn vì đã ủng hộ chúng tôi. Chúc bạn có những bữa ăn ngon miệng ^^.")
        return []

class ActionSorry(Action):
    def name(self) -> Text:
        return "action_sorry"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
                        text="Xin lỗi bạn vì bất tiện này. Chúng tôi luôn luôn cải thiện để phục vụ bạn.")
        return []