# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from foodData.connect import create_connection, get_shop_with_menu, get_location_of_shop, get_time_of_shop, get_shop_with_name,get_shop_with_location, get_shop_food_with_location

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet, UserUtteranceReverted, Restarted
from rasa_sdk.executor import CollectingDispatcher
import random
import gspread
from google.oauth2.service_account import Credentials

# from predict import Predictor

# predictor = Predictor()

# predictor.predict(
#     'bánh ga than thanh o dia chi nao')
con = create_connection()
# foodType = get_shop_with_menu(con, 'Pepsi')
# print(foodType)

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
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        location = get_location_of_shop(con, shop_name)
        if len(location):
            dispatcher.utter_message(
                text="Địa chỉ quán là: {} ạ.\nChúc anh/chị có bữa ăn ngon miệng ^^.".format(' '.join(location[0])))

        return []


class ActionGetTimeShop(Action):
    def name(self) -> Text:
        return "action_get_time_of_shop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        shop_name = next((x["value"] for x in tracker.latest_message['entities']
                          if x['entity'] == 'shop_name'), None)
        shop_arr = get_shop_with_name(con, shop_name)
        if len(shop_arr) == 1:
            dispatcher.utter_message(
                text="Quán {} có thời gian hoạt động: {} ạ.".format(shop_name, ' '.join(time[0])))
            return [SlotSet("has_one_shop","not")]
        elif len(shop_arr) == 0:
            dispatcher.utter_message(
                text="Quán {} không tồn tại. Bạn vui lòng kiểm tra lại nhé!".format(shop_name))
            return [SlotSet("has_one_shop","not")]
        else:
            dispatcher.utter_message(
                text="Bạn muốn hỏi cơ sở nào nhỉ:\n" + "\n".join(name[1] for name in shop_arr))
            return [SlotSet("has_one_shop","not")]

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
            result = get_shop_food_with_location(con,food_type, location)
            print(result)
            if(result is not None):
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" +  "\n".join("Tên quán: "+name[0]+ " địa chỉ: "+name[1]+","+name[2] for name in result))
            else:
                dispatcher.utter_message( text="Không tìm thấy quán")
        
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
            result = get_shop_food_with_location(con,food_name, location)
            print(result)
            if(result is not None):
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" +  "\n".join("Tên quán: "+name[0]+ " địa chỉ: "+name[1]+","+name[2] for name in result))
            else:
                dispatcher.utter_message( text="Không tìm thấy quán")
        
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
            result = get_shop_with_location(con,shop_name, location)
            if result is not None:
                dispatcher.utter_message(
                    text="Có các quán sau đây:\n" +  "\n".join("Tên quán: "+name[0]+ " địa chỉ: "+name[1]+","+name[2] for name in result))
            else:
                dispatcher.utter_message( text="Không tìm thấy")
        
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


class ActionStoreFoodName(Action):
    def name(self) -> Text:
        return "action_store_food_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(
            (x["value"] for x in tracker.latest_message['entities'] if x['entity'] == 'food_name'), None)
        return [SlotSet("shop_name", food_name)]


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


class ActionDataUpload(Action):
    def name(self):
      # type: () -> Text
        return "action_data_update"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict[Text, Any]]
        #   num = random.randint (0,99999)
        #   rating = int(tracker.get_slot('rating'))
        #   influence = tracker.get_slot('influence')
        #   support_feedback = tracker.get_slot('support_feedback')

        raw_update = [num, rating, influence, support_feedback]
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'foodassistant-idab-cd86eceaf949.json', scopes=scopes)
        clients = gspread.authorize(credentials)
        sheet = clients.open('foodorder').sheet1
        sheet.append_row(raw_update)

        response = 'I’m sharing the information on your behalf with our team. Have a nice day!'

        dispatcher.utter_message(response)
        return []


class getDataSheet(Action):
    def name(self):
        return "action_get_data_sheet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
                  'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'foodassistant-idab-c824a5211046.json', scopes=scopes)
        clients = gspread.authorize(credentials)
        sheet = clients.open_by_url(
            'https://docs.google.com/spreadsheets/d/1_wouCP-VaPtLGJ3GicsQnRo3gc07TTlij8a3nb2O9Mc/edit#gid=0').sheet1
        data = sheet.get_all_records()
        response = 'get success'
        buttons = [{
            "title": "Get location"
        }]

        message5 = {

            "text": "What do you want next?",
            "quick_replies": [
                {
                    "content_type": "user_phone_number"
                },
            ]
        }
        dispatcher.utter_message(json_message=message5)
        return []


class ActionUnknowns(Action):

    def name(self) -> Text:
        return "action_unknowns"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q='" +
            tracker.latest_message['text'].replace(" ", "%20") + "'")
        return []


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
            time_arr = get_time_of_shop(con,shop_name)
            print(time_arr)
            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại tôi chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để tôi nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q='" +
                tracker.latest_message['text'].replace(" ", "%20") + "'")
        return []