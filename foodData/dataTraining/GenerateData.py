import random


company = []
with open('food_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        company.append(line.strip())
f = open('food_name_intent.txt', 'w+', encoding='utf8')
for c in company:
    n = random.randint(0,59)
    f.write("""
- [shop_thaythe](food_name) giá bao nhiêu""".replace("shop_thaythe", c))
f.close()
