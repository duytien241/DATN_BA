<!-- ## order không thông tin 1
* order_food
  - action_store_food_type
  - slot{"has_food_type":"not"}
  - action_store_shop_name
  - slot{"has_shop_name":"not"}
  - action_ask_shop
* give_shop_name
  - action_get_shop
  - slot{"has_one_shop": "not"}
  - action_choose_shop
* give_shop_name
  - action_get_shop
  - slot{"has_one_shop": "has"}
  - action_ask_food_name
* give_food_name
  - action_get_food
  - slot{"has_one_food": "has"}
  - action_ask_quantity_order
* give_number
  - slot{"has_quantity_order": "has"}
  - action_ask_location_want_ship
* give_location
  - action_store_location
  - action_ask_phone_info
* customer_give_info
  - action_store_phone
  - action_ask_name
* give_name
  - action_store_cust_name
  - action_show_order_info
  - action_ask_confirm_order
* affirm
  - action_update_data
  - action_show_noti_order_success


## order không thông tin 1
* order_food
  - action_store_food_type
  - slot{"has_food_type":"not"}
  - action_store_shop_name
  - slot{"has_shop_name":"not"}
  - action_ask_shop
* give_shop_name
  - action_get_shop
  - slot{"has_one_shop": "not"}
  - action_choose_shop
* give_shop_name
  - action_get_shop
  - slot{"has_one_shop": "has"}
  - action_ask_food_name
* give_food_name
  - action_get_food
  - slot{"has_one_food": "has"}
  - action_ask_quantity_order
* give_number
  - slot{"has_quantity_order": "has"}
  - action_ask_location_want_ship
* give_location
  - action_store_location
  - action_ask_phone_info
* customer_give_info
  - action_store_phone
  - action_ask_name
* give_name
  - action_store_cust_name
  - action_show_order_info
  - action_ask_confirm_order
* affirm
  - action_update_data
  - action_show_noti_order_success -->
