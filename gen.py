import random
company = []
with open('./resources/food_name.txt', 'r+', encoding='utf8') as f:
    for line in f:
        company.append(line.strip())
f = open('AskTimeYesNoOfShopIntent.txt', 'w+', encoding='utf8')
i = 0
a = ''
b = ''
for c in company:
    i = i + 1
    if i % 2 ==0:
        f.write("""- lấy cho tôi [{}](number) [{}](food_name) với [{}](number) [{}](food_name)\n""".format(random.randint(3, 9), a, random.randint(3, 9), c))
    a = c
f.close()