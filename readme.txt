Bert————分类模型
- .idea————使用pycharm作为你的python编辑器的时候，你创建一个代码文件夹就会自动生成这个.idea文件夹。 这个文件夹的主要作用在于存放项目的控制信息，包括版本信息，历史记录等等
- bert-master————程序文件夹
	- .idea 【0】
	- __pycache__ 【0】————Python的缓存文件夹
	- .gitignore 【0】————IDEA或者Pycharm在提价代码到GIt时，经常会把项目根目录下的一些编译或输出文件自动添加进来，每次都得手动去掉勾选，十分浪费时间。为了解决此问题，GIt提供了.gitignore文件，来过滤不想提交的文件。
	- CONTRIBUTING.md 【0】
	- create_pretraining_data.py 【0】
	- divide_data.py 【2】————乱序数据集程序 
	- Evaluate_ahp.py 【0】————评测文件
    	- extract_features.py 【0】
	- final_result.txt 【1】————语音转文本的最终结果
	- LICENSE 【0】————软件许可证
	- main.py 【3】————一个未写完的端到端文件
	- modeling.py 【0】————模型文件 在别的程序文件里直接调用了
	- modeling_test.py【0】————模型测试文件 也是在别的文件里直接调用
	- multilingual.md【0】————说明信息
	- optimization.py 【0】
	-  optimization_test.py【0】
	- predicting_movie_reviews_with_bert_on_tf_hub.ipynb【0】
	- README.md【1】————原说明文件，可以看看
	- requirements.txt【1】————环境需求文件
	- result1.json【1】————语音转文本的初始文件，是json格式的
	- run_classifier.py【0】
	- run_classifier_with_tfhub.py【0】
	- run_pretraining.py【0】
	- run_squad.py【0】
	- sample_text.txt【0】————原样例文本
！！！！ - Step1_Wave2Text.py 【2】————第一步：语音转文本（调用讯飞API接口）
！！！！ - Step2_Text2Keywords.py【2】————第二步：文本提取关键词（调用讯飞API接口）
！！！！ - Step3_BertModel.py【2】————第三步：训练模型、预测结果
！！！！ - Step4_GetType.py【2】————第四步：由权重结果得最终分类结果， 获取测试集准确率
！！！！ - Step5_Evaluate_ew.py【2】————第五步：熵权法评测分类结果
	- test.mp4【1】————课堂视频，用作第一步数据源
	- test.wav【1】————课堂音频，视频转音频获得得结果
	- tokenization.py【0】
	- tokenization_test.py【0】
	- txt2tsv.py【2】————txt文件转写为tsv文件的程序（txt—>csv—>tsv），tsv文件为模型需要的文件，数据集处理的最后一步要用的
- glue ————存储文件夹
	- BERT_MODEL_DIR ———— 模型配置文件
	- glue_data ———— 数据集文件夹（这一块有点乱x）
	- math_outputs ———— 数学课的模型输出文件夹
	- chinese_outputs ———— 语文课的模型输出文件夹
	- download_glue_data.py ———— 下载其他开源nlp数据集
- chinese_predict ———— 语文课分类结果
	- pre_sample.tsv ————教师语音内容序列分类结果
	- test_results.tsv ————教师语音内容序列 权重结果
	- predict.tf_record 【0】
- math_predict ———— 数学课分类结果（同上）
- output ———— 第五步要用到的课堂语音分类结果 （每一个文件夹代表一堂课，最后输出的结果 是每堂课的类型）（目前做的属于粗分类，其实想做成一堂课一段时间内的评估）（这个文件夹应该是我一个一个采用txt2tsv.py文件转写得到的，有点笨，可以改一下txt2tsv.py文件，一下子全部撰写）（最后结果——教学类型 类别判断：1互动2灌输3讨论，好像是这样，记不太清了，这一块可以再看看）