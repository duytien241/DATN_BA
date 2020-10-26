## Chào - tên - hỏi chức năng - chào
* greet
  - action_hello
* ask_name
  - utter_ask_name
* ask_func_list
  - utter_func_list
* goodbye
  - utter_goodbye

## Chào  - hỏi chức năng - chào
* greet
  - utter_greet
* ask_func_list
  - utter_func_list
* goodbye
  - utter_goodbye

## Chào  - hỏi tên - chào
* greet
  - utter_greet
* ask_name
  - utter_ask_name
* goodbye
  - utter_goodbye

## Hỏi tên - hỏi chức năng
* ask_name
  - utter_ask_name
* ask_func_list
  - utter_func_list

## chào - hỏi quán ăn - tạm biệt
* greet
  - utter_greet
* give_shop_name{"shop_name":"Bánh mì vợ ong vàng"}
  - action_store_shop_name
  - action_show_location_shop
* goodbye
  - utter_goodbye

## chào - hỏi thông món ăn - tạm biệt
* greet
  - utter_greet
* ask_food_info
  - action_get_food_info
* goodbye
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## hỏi địa chỉ quán ăn
* ask_food_type_in_location{"location":"Đống Đa","food_type":"trà sữa"}
  - action_get_food_type_in_location

## hỏi địa chỉ quán ăn
* ask_location_of_shop
  - action_get_location_of_shop

## ask_yes_no_shop_with_time
* ask_yes_no_shop_with_time
  - action_yes_no_shop_with_time

## hỏi thời gian mở cửa
* ask_shop_with_time
  - action_get_time_of_shop

## hỏi địa chỉ quán có ở?
* ask_yes_no_food_info
  - action_yes_no_food_info

## hỏi thông tin giá món ăn 
* ask_food_price
  - action_get_food_price

## ask yes no trademark with location
* ask_yes_no_trademark_with_location
  - action_yes_no_trademark_with_location

## ask trademark with location
* ask_trademark_with_location
  - action_trademark_with_location

## ask yes no shop type with price
* ask_yes_no_shop_type_with_price
  - action_yes_no_shop_type_with_price