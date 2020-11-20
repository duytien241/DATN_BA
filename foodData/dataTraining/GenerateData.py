company = []
with open('shop_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        company.append(line.strip())
f = open('shop_name_intent.txt', 'w+', encoding='utf8')
for c in company:
    f.write("""
- quán [shop_thaythe](shop_name) có những gì""".replace("shop_thaythe", c))
f.close()
