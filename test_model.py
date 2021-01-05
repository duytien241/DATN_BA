import xlsxwriter
import datetime
import time
import requests
import json

stocks = []
with open('resources/shop_name.txt', 'r', encoding='utf8') as f:
    for line in f:
        stocks.append(line.strip())
    f.close()
 
with open('test/test_data.json', encoding='utf8') as json_file:
    data_test = json.load(json_file)

def test_stock():
    t  = 0
    for intent in data_test:
        workbook = xlsxwriter.Workbook('test/Result_{}_{}.xlsx'.format(intent,str(datetime.datetime.now().strftime('%d_%b_%G')))) 
        worksheet = workbook.add_worksheet()
        col1_name = 'Câu'
        col2_name = 'Itent_Correct'
        col3_name = 'Enteties_Correct'
        col4_name = 'Confident'
        col5_name = 'Intent'
        col6_name = 'Enteties'
        col7_name = 'Intent_soccer'
        col8_name = 'Enteties_soceer'
        worksheet.write('A1', col1_name) 
        worksheet.write('B1', col2_name) 
        worksheet.write('C1', col3_name) 
        worksheet.write('D1', col4_name) 
        worksheet.write('E1', col5_name)
        worksheet.write('F1', col6_name) 
        worksheet.write('G1', col7_name)
        worksheet.write('H1', col8_name)
        count_enteties = 0
        count_intent = 0
        count_enteties_correct = 0
        count_intent_correct = 0
        for sentence in data_test[intent]:
            print(sentence)
            for i in range(len(stocks)):
                t = t + 1
                sentence_tmp = sentence
                count = 0
                if i == 100:
                    break
                while sentence_tmp.find("[") and count == 0:
                    count = count + 1
                    start = sentence_tmp.find("[")
                    end = sentence_tmp.find(")")
                    start_enteties = sentence_tmp.find("(")
                    enteties = "\'entity\': \'{}\', \'start\': {}, \'end\': {}".format(sentence_tmp[start_enteties+1:end],start,start+len(stocks[i]))
                    sentence_tmp = sentence_tmp.replace(sentence_tmp[start:end+1], stocks[i])
                    print(sentence_tmp)
                    worksheet.write('A{}'.format(t+2), sentence_tmp)
                    worksheet.write('B{}'.format(t+2), intent)
                    worksheet.write('C{}'.format(t+2), enteties) 
                    response = requests.post("http://localhost:5005/model/parse",json={'text': sentence_tmp})
                    if response.status_code == 200:
                        json_data = json.loads(response.text)
                        count_intent = count_intent + 1
                        count_enteties = count_enteties + 1
                        enteties_res = str(json_data['entities'])
                        if enteties_res.find(enteties) != -1:
                            worksheet.write('H{}'.format(t+2), 1)
                            count_enteties_correct = count_enteties_correct + 1
                        else:
                            worksheet.write('H{}'.format(t+2), 0)
                        worksheet.write('D{}'.format(t+2), json_data["intent"]["confidence"])
                        print(json_data["intent"]["confidence"])
                        worksheet.write('E{}'.format(t+2), json_data["intent"]["name"])
                        worksheet.write('F{}'.format(t+2), enteties_res)
                        if json_data["intent"]["name"] == intent:
                            worksheet.write('G{}'.format(t+2), 1)
                            count_intent_correct = count_intent_correct + 1
                        else:
                            worksheet.write('G{}'.format(t+2), 0)
        print(count_intent)
        worksheet.write('I1'.format(count_intent+2), "Độ chính xác itent:{0:.2f}%".format(count_intent_correct/count_intent*100))
        worksheet.write('I2'.format(count_enteties+2), "Độ chính xác ner:{0:.2f}%".format(count_enteties_correct/count_enteties*100))
        workbook.close() 

if __name__ == "__main__":
    test_stock()