import os
import pandas as pd


if __name__ == '__main__':
    path = "..\\math_predict"
    pd_all = pd.read_csv(os.path.join(path, "test_results.tsv") ,sep='\t',header=None)

    data = pd.DataFrame(columns=['class'])

    for index in pd_all.index:
        one_score = pd_all.loc[index].values[0]
        two_score = pd_all.loc[index].values[1]
        three_score = pd_all.loc[index].values[2]
        four_score = pd_all.loc[index].values[3]
        five_score = pd_all.loc[index].values[4]
        six_score = pd_all.loc[index].values[5]
        seven_score = pd_all.loc[index].values[6]

        if max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == one_score:
            data.loc[index+1] = ["0"]
        elif max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == two_score:
            data.loc[index+1] = ["1"]
        elif max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == three_score:
            data.loc[index+1] = ["2"]
        elif max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == four_score:
            data.loc[index+1] = ["3"]
        elif max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == five_score:
            data.loc[index+1] = ["4"]
        elif max(one_score,two_score,three_score,four_score,five_score,six_score,seven_score) == six_score:
            data.loc[index+1] = ["5"]
        else:
            data.loc[index+1] = ["6"]

    data.to_csv(os.path.join(path, "pre_sample.tsv"),sep = '\t')

    fpath = "E:\\cv_work_3\\Bert\\glue\\glue_data\\Math_TACdata\\test.tsv"
    test = pd.read_csv(fpath,sep='\t')
    count = 0
    for i in range(len(test)):
        if(int(test['id'][i])==int(data.loc[i+1])):
            count = count+1
    print("bert_accuracy:",count/len(test))


