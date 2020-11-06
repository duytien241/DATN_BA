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

## hỏi địa chỉ loại quán ăn: có quán bành mì nào ngon ở Thái Hà không
* ask_food_type_in_location
  - action_get_food_type_in_location

## hỏi địa chỉ với quán ăn
* ask_location_of_shop
  - action_get_location_of_shop

## hỏi thời gian hoạt động của cửa hàng với tên 2
* ask_shop_with_time
  - action_get_time_of_shop
* give_shop_name{"has_one_shop": "not"}
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động
* ask_yes_no_shop_with_time
  - action_yes_no_shop_with_time

## hỏi yes no về thời gian hoạt động2
* ask_yes_no_shop_with_time
  - action_yes_no_shop_with_time
* give_shop_name{"has_one_shop": "No"}
  - action_yes_no_shop_with_time

## hỏi địa chỉ quán có ở?: món trà sữa to co có ở X không
* ask_yes_no_food_info_location
  - action_yes_no_food_info_location

## hỏi thông tin món ăn 
* ask_food_info
  - action_get_food_info

## hỏi thông tin giá món ăn 
* ask_food_price
  - action_get_food_price

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
  - action_show_fee_ship

## hỏi cửa hàng [Bánh mỳ vợ ong vàng](shop_name) có ship về [Thái hà](location) không?
* ask_yes_no_ship_with_shop_and_location
  - action_show_shop_ship

# hỏi: cửa hàng [Bánh mỳ vợ ong vàng](shop_name) phí ship bao nhiêu?
* ask_ship_with_shop
  - action_show_avg_ship

# hỏi: cửa hàng [Bánh mỳ vợ ong vàng](shop_name) có freeship không?
* ask_yes_no_free_ship_with_shop
  - action_show_free_ship

## đặt hàng
* order_food_type
  - action_store_food_type
  - action_show_list_shop_match
* give_shop_name
  - action_store_shop_name
  - action_ask_shop_location_cus_want
* give_location_shop
  - action_store_location_shop
  - action_ask_food_name
  - action_show_food_list
* give_food_name
  - action_store_food_name
  - action_ask_quantity_order
* give_number
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

