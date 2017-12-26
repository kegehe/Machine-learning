# -*- coding:utf-8 -*-
import os
import re

#加载训练集，用于分词，制作单词词典(word,count)
def traination(path):
    list = {}
    os.chdir(path)
    long = len(os.listdir('./'))
    for x in os.listdir('./'):
        with open(x,encoding='ISO-8859-15') as file:
            lines = file.readlines()
            for x in lines:
                word = x.strip().split(' ')
                for y in word:
                    if len(y) < 3 or y.isdigit():   #过滤小于3个单位的单词和数字
                        continue
                    if y in list.keys():
                        list[y] = list[y] + 1   #重复的单词就加1
                    else:
                        list[y] = 1 #没有在列表中出现过的单词则创建
    return list,long

#加载测试机，用于分词，制作单词词典(word,count)，并进行测试
def prediction(path):
    os.chdir(path)
    label = []
    i = 0
    erro = 0
    for x in os.listdir('./'):
        predict_wordlist = {}
        label.append(re.search(r"spam|ham",x).group())  #从文件名中分割出实际结果的标签
        with open(x, encoding='ISO-8859-15') as predict:
            lines = predict.readlines()
            totall = 0
            for y in lines:
                word = y.strip().split(' ')
                for z in word:
                    if len(z) < 3 or z.isdigit():
                        continue
                    if z in predict_wordlist.keys():
                        predict_wordlist[z] = predict_wordlist[z] + 1
                    else:
                        predict_wordlist[z] = 1
                    totall = totall + 1
            result = predic(predict_wordlist)
            print(r'预测结果：',predic(predict_wordlist),'；',r'实际结果：',label[i])
        if result != label[i]:
            erro = erro + 1
        i = i + 1
    print(r'准确率：', 1-(erro / len(label)),r'；测试样本：',len(label),r'错误样本：',erro)

#计算邮件是垃圾邮件的概率
def predic(list):
    ps = longofham/longofham+longofspam
    ph = longofspam/longofham+longofspam
    p = []
    for x in list.keys():
        if x in ham_wordlist.keys() and x in spam_wordlist.keys():
            pws = ham_wordlist[x] / 1981031 #计算P(w|h),在是垃圾邮件的情况下,该词出现的概率
            pwh = spam_wordlist[x] / 525681 #计算P(w|s),在非垃圾邮件的情况下，该词出现的概率
            pham = pws * ps / (pws * ps + ph * pwh) #计算P(s|w),计算出现该词的情况下,该文件是垃圾邮件的概率
            p.append(pham)
    #利用联合分布概率来计算所有的词在该邮件中,该邮件是垃圾邮件的概率
    #p(s|w1)*p(s|w2)···*p(s)/p(s|w1)*p(s|w2)···*p(s)+(1-p(s|w1))*(1-p(s|w2))*···*(1-p(s))
    top = 1
    down = 1
    for x in p:
        top = x*top
        down = down*(1-x)
    return 'ham' if top/(top+down) > 0.9 else 'spam'    #是垃圾邮件的概率大于0.9则认为是垃圾邮件

#----------------------------分割线------------------------------------

ham = 'C:\\Users\\12259\\Desktop\\TestFile\\DataSet\\Naive_Bayesian\\email\\train\\ham'  #垃圾邮件目录
spam = 'C:\\Users\\12259\\Desktop\\TestFile\\DataSet\\Naive_Bayesian\\email\\train\\spam'    #非垃圾邮件目录
test = 'C:\\Users\\12259\\Desktop\\TestFile\\DataSet\\Naive_Bayesian\\email\\test\\classfiy' #测试目录

ham_wordlist,longofham = traination(ham)
spam_wordlist,longofspam = traination(spam)

prediction(test)