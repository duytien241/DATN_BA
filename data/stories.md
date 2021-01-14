## chào hỏi
* greet
  - action_hello

## tạm biệt
* goodbye
  - action_goodbye

## hỏi chức năng
* ask_func_list
  - action_show_func

## xin gợi ý
* request_for_suggestion
  - action_recommend

## hỏi địa chỉ với quán ăn cửa hàng với tên 
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn với tên cùng 1 trademark
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn của cửa hàng với tên 2
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn của cửa hàng với tên xác nhận
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn của cửa hàng với tên 3
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn của cửa hàng với tên 3 - đưa địa chỉ
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_location_of_shop

## hỏi địa chỉ với quán ăn của cửa hàng với tên 3 - đưa địa chỉ - gợi ý
* ask_location_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_location_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên 
* ask_time_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_time_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên cùng 1 trademark
* ask_time_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_time_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên 2
* ask_time_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_time_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên 2 - gợi ý
* ask_time_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_time_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên 3
* ask_time_of_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_time_of_shop

## hỏi yes no về thời gian hoạt động có 1 shop
* ask_yes_no_shop_with_time
  - action_store_time
  - slot{"has_time": "has"}
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động có 1 shop không có thời gian
* ask_yes_no_shop_with_time
  - action_store_time
  - slot{"has_time": "not"}
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_yes_no_shop_with_time
* give_time
  - action_store_time
  - slot{"has_time": "not"}
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động
* ask_yes_no_shop_with_time
  - action_store_time
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động2
* ask_yes_no_shop_with_time
  - action_store_time
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động2 - gợi ý
* ask_yes_no_shop_with_time
  - action_store_time
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_yes_no_shop_with_time

## hỏi có hoạt động của cửa hàng với tên 2
* ask_yes_no_shop_with_time
  - action_store_time
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_yes_no_shop_with_time

## hỏi thương hiệu này có ở X ko
* ask_yes_no_trademark_with_location
  - action_yes_no_trademark_with_location

## hỏi thương hiệu với địa điểm: [tocotoco](trademark) có mấy cơ sở ở [Hà Nội](location)?
* ask_number_trademark_with_location
  - action_number_trademark_with_location

## hỏi shop với mức giá 
* ask_yes_no_shop_type_with_price
  - action_yes_no_shop_type_with_price

## hỏi ship
* ask_ship_with_shop_and_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_show_fee_ship

## hỏi cửa hàng [Bánh mỳ vợ ong vàng](shop_name) có ship về [Thái hà](location) không?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_store_location
  - slot{"has_location":"not"}
  - action_ask_location
* give_location
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"not"}
  - action_show_shop_ship

## hỏi cửa hàng ship với tên?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_store_location
  - slot{"is_near":"not"}
  - action_show_shop_ship

## hỏi cửa hàng ship với không tên?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"is_near":"not"}
  - action_show_shop_ship


## hỏi cửa hàng ship với không tên- không địa điểm
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"has_location": "not"}
  - action_ask_location
* give_location
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"not"}
  - action_show_shop_ship

## hỏi cửa hàng ship với không tên 2?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"is_near":"not"}
  - action_show_shop_ship

## hỏi cửa hàng ship với không tên - đồng ý?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - slot{"is_near":"not"}
  - action_show_shop_ship

## hỏi cửa hàng ship với không tên và gần đây? 2
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"is_near":"has"}
  - slot{"has_address":"has"}
  - action_show_shop_ship

## hỏi cửa hàng ship với không tên và gần đây?
* ask_ship_with_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_location
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"is_near":"has"}
  - slot{"has_address":"not"}
  - action_ask_location
* give_location
  - action_store_current_address
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"not"}
  - action_show_shop_ship


# hỏi: cửa hàng [Bánh mỳ vợ ong vàng](shop_name) có freeship không?
* ask_yes_no_ship_with_shop_and_location
  - action_show_free_ship

## đặt món rõ thông tin cửa hàng
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "has"}
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 1.1
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 2
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 3s
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 3s
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 4s
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 4s-2
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_food_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}


## đặt món ăn chưa rõ thông tin 5s
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 6
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_check_food
  - order_form
  - form{"name": "order_form"}
  - form{"name": null}

## đặt món ăn chưa rõ thông tin 6 -fail 1
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_retry

## đặt món ăn chưa rõ thông tin 6 - fail 2
* order_food
  - action_store_has_one_shop
  - action_save_info_order
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_retry

## Hỏi thông tin cửa hàng
* ask_information_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - ation_ask_information_shop

## Hỏi thông tin cửa hàng 2
* ask_information_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - ation_ask_information_shop


## Hỏi thông tin cửa hàng 3
* ask_information_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_choosen_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - ation_ask_information_shop

## hỏi menu hoạt động của cửa hàng với tên 
* ask_menu_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_menu_shop

## hỏi menu hoạt động của cửa hàng với tên 3
* ask_menu_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_menu_shop

## hỏi menu hoạt động của cửa hàng với tên 3-2
* ask_menu_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_menu_shop

## hỏi menu hoạt động của cửa hàng với tên 3 - gợi ý
* ask_menu_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_menu_shop

## Hỏi quán ở khu vực 1.1
* ask_shop_with_info
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"has"}
  - slot{"has_address":"has"}
  - action_store_time
  - action_store_shop_type
  - action_get_shop_in_location

## Hỏi quán ở khu vực 1
* ask_shop_with_info
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"has"}
  - slot{"has_address":"not"}
  - action_store_time
  - action_store_shop_type
  - action_ask_location
* give_location
  - action_store_current_address
  - action_store_location
  - slot{"has_location":"has"}
  - action_get_shop_in_location

## Hỏi quán ở khu vực 2
* ask_shop_with_info
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"not"}
  - action_get_shop_in_location

## Hỏi quán ở khu vực 3
* ask_shop_with_info
  - action_store_location
  - slot{"has_location":"not"}
  - slot{"is_near":"not"}
  - action_store_time
  - action_store_shop_type
  - action_ask_location
* give_location
  - action_store_location
  - slot{"has_location":"has"}
  - slot{"is_near":"not"}
  - action_get_shop_in_location
  
## hỏi thông tin giá món ăn 
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn 2
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_store_has_food_name
  - slot{"has_food_name": "not"}
  - action_get_food_price
* give_food_name
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  3
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  32
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_has_food_name
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  3 - gợi ý
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_has_food_name
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_food_price

## hỏi thông tin giá món ăn  3 - gợi ý
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - action_store_has_food_name
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"has_food_name": "not"}
  - action_ask_food_name
* give_food_name
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  3 - gợi ý 2
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - action_store_has_food_name
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - action_has_one_trademark
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - slot{"has_food_name": "not"}
  - action_ask_shop
* action_ask_food_name
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  3
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_store_has_food_name
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - action_has_one_trademark
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_food_price

## hỏi thông tin giá món ăn  32
* ask_food_price
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - action_store_has_food_name
  - slot{"has_food_name": "has"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - action_has_one_trademark
  - slot{"has_one_shop": "not"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_food_price

## đưa thông tin địa điểm
* give_location
  - action_store_location
  - slot{"has_location":"has"}
  - action_ask_for_location

## hỏi thông tin đơn hàng
* ask_status_order
  - action_get_status_order

## hỏi hỏi thông tin shop với tên 
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop với tên cùng 1 trademark
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 2
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên xác nhận
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 3
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_shop_name
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 3 - đưa địa chỉ
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* give_location
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 3 - đưa địa chỉ - gợi ý
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
  - slot{"has_recom": "has"}
* say_yes
  - action_replace_recommendation
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 3 - đưa địa chỉ - gợi ý 2
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* deny
  - action_store_deny
  - action_ask_shop
* give_shop_name
  - action_store_deny
  - action_store_has_one_shop
  - slot{"has_one_shop": "has"}
  - action_get_option_shop

## hỏi hỏi thông tin shop của cửa hàng với tên 3 - đưa địa chỉ - gợi ý 3
* ask_option_shop
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"not"}
  - action_ask_shop
* deny
  - action_store_deny
  - action_ask_shop
* give_shop_name
  - action_store_deny
  - action_store_has_one_shop
  - slot{"has_one_shop": "not"}
  - action_has_one_trademark
  - slot{"has_in_one_trademark":"has"}
  - action_get_option_shop

## Từ chối
* deny
  - ation_deny

## Cảm ơn
* thankyou 
  - action_thanks

## gợi ý
* ask_recommnend_food 
  - action_recommend

## khen
* give_comment_neg 
  - action_thanks

## che
* give_comment_pos
  - action_sorry