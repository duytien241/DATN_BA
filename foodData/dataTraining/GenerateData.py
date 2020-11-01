company = []
with open('shop_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        company.append(line.strip())
f = open('shop_name_intent.txt', 'w+', encoding='utf8')
for c in company:
    f.write("""
- quán [bánh mì Vợ ong vàng](shop_name) ở đâu?
- quán [bánh mì Vợ ong vàng](shop_name) ở địa chỉ nào?
- quán [bánh mì Vợ ong vàng](shop_name) ở chỗ nào?
- quán [bánh mì Vợ ong vàng](shop_name) bán chỗ nào?
- quán [bánh mì Vợ ong vàng](shop_name) bán ở chỗ nào?
- địa chỉ quán [bánh mì Vợ ong vàng](shop_name)?
- địa chỉ [bánh mì Vợ ong vàng](shop_name)?
- cửa hàng [bánh mì Vợ ong vàng](shop_name) ở chỗ nào ?
- cho mình hỏi quán [bánh mì Vợ ong vàng](shop_name) ở đâu vậy?
- cho mình xin địa chỉ cụ thể quán [bánh mì Vợ ong vàng](shop_name)
- địa chỉ của quán [bánh mì Vợ ong vàng](shop_name) ở đâu?
- cửa hàng [bánh mì Vợ ong vàng](shop_name) ở địa chỉ nào?
- cửa hàng [bánh mì Vợ ong vàng](shop_name) ở đâu?
- địa chỉ của cửa hàng [bánh mì Vợ ong vàng](shop_name) ở đâu?
- quán [bánh mì Vợ ong vàng](shop_name) ở đâu nhỉ ?
- ad ơi cho em hỏi quán [bánh mì Vợ ong vàng](shop_name) ở đâu thế nhỉ?
- cửa hàng [bánh mì Vợ ong vàng](shop_name) thế ?
- quán [bánh mì Vợ ong vàng](shop_name) ở đâu?
- cho mình địa chỉ quán [bánh mì Vợ ong vàng](shop_name)?
- bạn ơi quán quán [bánh mì Vợ ong vàng](shop_name) ở đâu? 
- cho tôi hỏi của hàng [bánh mì Vợ ong vàng](shop_name) ở đâu vậy?""".replace("bánh mì Vợ ong vàng", c))
f.close()
