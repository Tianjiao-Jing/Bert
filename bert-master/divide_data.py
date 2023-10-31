import os
import random
out = open("F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/TAC/Math_TAC2.0.txt",'w',encoding='utf-8')
lines=[]
with open("F:/BNU/YanyYiShang/Project/Bert/glue/glue_data/TAC/Math_TAC.txt", 'r',encoding='utf-8') as infile:
    for line in infile:
        lines.append(line)
    random.shuffle(lines)
    for line in lines:
        out.write(line)

