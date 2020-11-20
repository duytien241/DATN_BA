# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
from django.db.models import Count
from typing import Dict, Text, Any, List, Union, Optional
from foodData.connect import create_connection, get_shop_with_menu, get_location_of_shop, get_time_of_shop, get_shop_with_name, get_shop_with_location, get_shop_food_with_location, get_food_with_name
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, UserUtteranceReverted, Restarted
from rasa_sdk.executor import CollectingDispatcher
import random
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from app.models import Address, TimeOpen, Restaurant, MenuItem, Order, OrderDetail, District
from utils.common import getTimeOpenInTradeMark, checkInOneTradeMark, getLocationOfShop, getMenuOfRestaurant, getShopWithInfo
# from predict import Predictor

con = create_connection()


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
        buttons = [{
            "type": "location", "title": "Get location"
        }]
        dispatcher.utter_message(text=response, buttons=buttons)
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
        dispatcher.utter_message(text="Tôi có thể giúp bạn gợi ý món ăn?")

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


class ActionGetLocationShop(Action):
    def name(self) -> Text:
        return "action_get_location_of_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name_slot = tracker.get_slot("shop_name")
        trademark_slot = tracker.get_slot("trademark")
        if trademark_slot is not None and trademark_slot in shop_name_slot:
            shop_name = trademark_slot
        else:
            shop_name = next((x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'shop_name'), None)
        location = next((x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        list_location = getLocationOfShop(shop_name,location)
        if len(list_location) == 1 and location is not None:
            dispatcher.utter_message(
                text="Địa chỉ quán tại {} là: {} ạ.\nChúc anh/chị có bữa ăn ngon miệng ^^.".format(location, list_location[0].address_full))
            return [SlotSet("shop_name",list_location[0].restaurant)]
        elif location is None and len(list_location) == 1:
            dispatcher.utter_message(
                text="Địa chỉ quán là: {} ạ.\nChúc anh/chị có bữa ăn ngon miệng ^^.".format(list_location[0].address_full))
        elif len(list_location) > 1:
            dispatcher.utter_message(
                text="Có quá nhiều kết quả khớp. Vui lòng kiểm tra lại tên quán nhé bạn")
        else:
            dispatcher.utter_message(text="Không có kết quả phù hợp. Vui lòng kiểm tra lại tên quán nhé bạn")
        return []


class ActionGetShop(Action):
    def name(self) -> Text:
        return "action_get_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        shop_arr = get_shop_with_name(con, shop_name)
        if len(shop_arr) == 1:
            return [SlotSet("has_one_shop", "has")]
        elif len(shop_arr) == 0:
            return [SlotSet("has_one_shop", "not")]
        else:
            return [SlotSet("has_one_shop", "not")]

class ActionsHasOneTradeMark(Action):
    def name(self) -> Text:
        return "action_has_one_trademark"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        if str(shop_name).lower() in list_trademark:
            return [SlotSet("has_in_one_trademark", "has")]
        else:
            return [SlotSet("has_in_one_trademark", "not")]

class ActionsHasOneTradeMarkShop(Action):
    def name(self) -> Text:
        return "action_store_has_one_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        if shop_name is None:
            shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'food_name'), None)
        location = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'location'), None)
        list_shop = getLocationOfShop(shop_name, location)
        if len(list_shop) == 1:
            return [SlotSet("has_one_shop", "has"), SlotSet("shop_name", list_shop[0].restaurant.name)]
        else:
            return [SlotSet("has_one_shop", "not"), SlotSet("shop_name", None)]


class ActionGetFood(Action):
    def name(self) -> Text:
        return "action_get_food"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        food_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'food_name'), None)
        food_arr = get_food_with_name(con, food_name)
        if len(food_arr) == 1:
            return [SlotSet("has_one_food", "has")]
        elif len(food_arr) == 0:
            return [SlotSet("has_one_food", "not")]
        else:
            return [SlotSet("has_one_food", "not")]


class ActionGetTimeShop(Action):
    def name(self) -> Text:
        return "action_get_time_of_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['entities'])
        # shop_name_chat = next((x["value"] for x in tracker.latest_message['entities']
        #                   if x['entity'] == 'shop_name'), None)
        # shop_name_slot = tracker.get_slot("shop_name")
        shop_name = tracker.get_slot("shop_name")
        if shop_name is None:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thời gian mở cửa của cửa hàng nào?")
            return [SlotSet("has_one_shop", "not"), ]
        shop_arr = Restaurant.objects.filter(name=shop_name)
        if len(shop_arr) == 1:
            if shop_arr[0].time_open.has_two_shift:
                dispatcher.utter_message(
                    text="Quán {} mở cửa từ {} tới {} và từ {} tới {} ạ."
                        .format(shop_name, 
                            shop_arr[0].time_open.shift_one_start, 
                            shop_arr[0].time_open.shift_one_end,
                            shop_arr[0].time_open.shift_two_start,
                            shop_arr[0].time_open.shift_two_end,))
            else:
                dispatcher.utter_message(
                    text="Quán {} mở cửa từ {} tới {} ạ.".format(shop_name, shop_arr[0].time_open.shift_one_start, shop_arr[0].time_open.shift_one_end))
            return [SlotSet("has_one_shop", "has")]
        elif len(shop_arr) == 0:
            dispatcher.utter_message(
                text="Quán {} không tồn tại. Bạn vui lòng kiểm tra lại nhé!".format(shop_name))
            return [SlotSet("has_one_shop", "not")]
        elif checkInOneTradeMark(shop_arr):
            message = 'Quán {} có các cơ sở với thời gian mở cửa sau:\n'.format(shop_arr[0].trademark.name)
            res = getTimeOpenInTradeMark(shop_arr, True)
            for item in res:
                if item.has_two_shift:
                    message  = message + "Cơ sở {} mở cửa từ {} tới {} và từ {} tới {}.\n".format(', '.join(res[item]), 
                                                                                        item.shift_one_start, 
                                                                                        item.shift_one_end,
                                                                                        item.shift_two_start,
                                                                                        item.shift_two_end,)
                else:
                    message = message + "Các Cơ sở {} mở cửa từ {} tới {}.\n".format(', '.join(res[item]), item.shift_one_start, item.shift_one_end)
            dispatcher.utter_message(text=message)
            return [SlotSet("has_one_shop", "not"),SlotSet("email", "not")]
            # dispatcher.utter_message(
            #     text="Bạn muốn hỏi cơ sở nào nhỉ:\n" + "\n".join(i.name for i in shop_arr))
        else:
            dispatcher.utter_message(
                text="Có khá nhiều cửa hàng với từ khóa mà bạn tìm kiếm.Bạn vui lòng kiểm tra lại nhé.")
            return [SlotSet("has_one_shop", "not")]


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
            print(result)
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


class ActionGetYesNoShopWithTime(Action):
    def name(self) -> Text:
        return "action_yes_no_shop_with_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="Quán {} không hoạt động")
        else:
            dispatcher.utter_message(
                text="Quán {} có hoạt động")

        return []


class ActionGetFoodPrice(Action):
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
            result = get_shop_food_with_location(con, food_name, location)
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
            result = get_shop_with_location(con, shop_name, location)
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
        return "action_show_shop_ship"

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


class ActionShowAvgShip(Action):
    def name(self) -> Text:
        return "action_show_avg_ship"

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


class ActionShowFreeShip(Action):
    def name(self) -> Text:
        return "action_show_free_ship"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = None
        if(result == None):
            dispatcher.utter_message(
                text="Quán {} không thấy")
        else:
            dispatcher.utter_message(
                text="Quán {} free ship")

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
        shop_arr = get_shop_with_name(con, shop_name)
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


class ActionStoreLocation(Action):
    def name(self) -> Text:
        return "action_store_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'location'), None)
        return [SlotSet("location", location)]


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

        time = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'time'), None)
        return [SlotSet("time", time)]


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
        shop_name = shop_name_chat if shop_name_chat is not None else shop_name_slot
        time = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'cust_name'), None)
        if shop_name is not None:
            time_arr = get_time_of_shop(con, shop_name)
            print(time_arr)
            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q='" +
                tracker.latest_message['text'].replace(" ", "%20") + "'")
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
            time_arr = get_time_of_shop(con, shop_type)
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
            text="action_ask_shop'" +
            tracker.latest_message['text'].replace(" ", "%20") + "'")
        return []


class OrderFormInfo(FormAction):

    def name(self) -> Text:

        return "order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["shop_name", "food_name", "quantity_order", "cust_nane", "address", "phone", "email"]

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
                    dispatcher.utter_template("utter_ask_{}".format(slot),
                                              tracker,
                                              silent_fail=False,
                                              **tracker.slots)
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
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                     if x['entity'] == 'shop_name'), None)
        if shop_name and str(shop_name).lower() in list_shop_name:
            return {"shop_name": shop_name}
        else:
            dispatcher.utter_message(
                text="Tên quán không tồn tại. Vui lòng kiểm tra và nhập lại")
            return {"shop_name": None}

    def validate_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        email = re.search(
            "[A-Za-z0-9_.]{4,32}@([a-zA-Z0-9]{2,12})(.[a-zA-Z]{2,12})+", value)
        if (tracker.latest_message['intent']['name'] == 'exit_form'):
            return None
        if (tracker.latest_message['intent']['name'] == 'hoi_sao_can_thong_tin'):
            dispatcher.utter_message(
                text="Dạ Bot cần thông tin để đặt vé và liên lạc lạc với quý khách ạ. Tất cả thông tin quý khách cung câp được bảo mật tuyệt đối ạ!")
            return {"email": None}
        if not email:
            dispatcher.utter_message(
                text="Email không hợp lệ! Mời quý khách kiểm tra lại.")
            return {"email": None}
        else:
            email = email.group()
            return {"email": email}

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
        if not phone:
            dispatcher.utter_message(
                text="Số điện thoại không hợp lệ! Mời quý khách kiểm tra lại.")
            return {"phone": None}
        else:
            phone = phone.group()
            return {"phone": phone}

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "email": self.from_text(),
            "phone": self.from_text(),
            "full_name": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""
        index_choice = int(tracker.get_slot("fl_choice")) - 1
        depart = tracker.get_slot("from")
        to = tracker.get_slot("to")
        numP = tracker.get_slot("num_of_people")
        date_value = tracker.get_slot("time")
        total_price = 0
        dispatcher.utter_message(text="THÔNG TIN ĐẶT VÉ:\n")
        if tracker.get_slot("airline_dislike") is None:
            airline_dislike = []
        else:
            airline_dislike = tracker.get_slot("airline_dislike")
        listFlight = getFlight.searchFlight(
            depart, to, date_value, airline_dislike)
        for fl in listFlight[index_choice]["flight"]:
            price = int(numP)*fl["gia_ve"]
            total_price += price
            flightText = "CHUYẾN BAY {:<20} {}({})-{}({}) \n  Giờ đi: {}  -  Giờ đến: {}\n  Giá vé: {:,} x {} = {:,} VNĐ\n".format(
                fl["ten_chuyen_bay"], fl["ten_san_bay_di"], fl['tinh_di'], fl["ten_san_bay_den"], fl["tinh_den"],
                format_date.convertDateStr(fl["ngay_gio_di"]), format_date.convertDateStr(fl["ngay_gio_den"]), fl["gia_ve"], numP, price)
            dispatcher.utter_message(text=flightText)
        dispatcher.utter_message(
            text="Tổng cộng: {:,} VND\n".format(total_price))
        f_name = tracker.get_slot("full_name")
        phone = tracker.get_slot("phone")
        email = tracker.get_slot("email")
        dispatcher.utter_message(
            text="Tên: {}\nSĐT: {}\nEmail: {}".format(f_name, phone, email))
        dispatcher.utter_message(
            text="Bot đã lưu lại thông tin đặt vé và sẽ sớm liên lạc lại với quý khách!")
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
        menu = getMenuOfRestaurant(shop_name)
        if len(menu) == 0 and shop_name is not None:
            dispatcher.utter_message(
                text="Menu của quá {} chưa được cập nhật".format(shop_name))
        elif len(menu) != 0 and shop_name is not None:
            dispatcher.utter_message(
                text="Quán {} có các món sau đây: {}".format(shop_name, "\n".join(item.name for item in menu )))
        return []

class ActionAskLocation(Action):

    def name(self) -> Text:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = tracker.get_slot("shop_name")
        return [FollowupAction(name='action_get_shop_in_location')]

class ActionsHasLocation(Action):
    def name(self) -> Text:
        return "action_has_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        location = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'location'), None)
        if location is not None:
            return [SlotSet("has_location", "has"), SlotSet("location", location)]
        else:
            return [SlotSet("has_location", "not"), SlotSet("location", None)]

class ActionGetShopWithInfo(Action):
    def name(self) -> Text:
        return "action_get_shop_in_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.get_slot("location"))
        print(tracker.get_slot("time"))
        print(tracker.get_slot("shop_type"))
        getShopWithInfo(location = 'Bách Khoa')
        return []