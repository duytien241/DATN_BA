AEIOUYD_VN = list("áàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệiíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵđ")
A_LIST = list("aáàảãạăắằẳẵặâấầẩẫậ")
E_LIST = list("eéèẻẽẹêếềểễệ")
I_LIST = list("iíìỉĩị")
O_LIST = list("oóòỏõọôốồổỗộơớờởỡợ")
U_LIST = list("uúùủũụưứừửữự")
Y_LIST = list("yýỳỷỹỵ")
D_LIST = list("dđ")

text= 'hôm nay là thu 6 ngay 13'
arr = text.split(' ')
count = 0
for i in arr:
    for t in i:
        if t in AEIOUYD_VN:
            count = count + 1

print(count/len(arr))
print(int('16,000đ'.replace(",","").replace("đ","")))
