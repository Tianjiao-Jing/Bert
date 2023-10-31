import csv

csvFile = open("F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/Math_TACdata/test.csv", 'w', newline='', encoding='utf-8')
writer = csv.writer(csvFile)
csvRow = []

f = open("F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/Math_TACdata/test.txt", 'r', encoding='utf8')
for line in f:
    csvRow = line.split()
    temp_label = csvRow.pop()  # 得到最后一个元素
    csvRow = ["".join(csvRow), temp_label]  # join合并元素
    writer.writerow(csvRow)
f.close()
csvFile.close()

# # 转成tsv文件
with open('F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/Math_TACdata/test.csv', encoding='utf-8') as f:
    data = f.read().replace(',', '\t')
with open('F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/Math_TACdata/test.tsv', 'w', encoding='utf-8') as f:
    f.write(data)
f.close()