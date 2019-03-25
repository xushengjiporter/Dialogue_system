# -*- coding: utf-8 -*-
import re,jieba
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import shuffle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn import svm
comments_new=[]
tfidf2=TfidfVectorizer(analyzer="word")


def remove_punctuation(line, strip_all=True):
  if strip_all:
    rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
    line = rule.sub('',line)
  else:
    punctuation = """，！？。＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏ """
    punctuation_en="""!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    re_punctuation = "[{}]+".format(punctuation)
    re_punctuation_en = "[{}]+".format(punctuation_en)
    line = re.sub(re_punctuation, "", line)
    line=re.sub(re_punctuation_en,"",line)
  return line.strip()

def cutline(line):
    line=str(line)
    words=jieba.cut(line,cut_all=False)
    re=" ".join(words)
    return re

def get_stopwords(line):
    f=open("F:\pre_trained\stopwords.txt")
    stopwords=[]
    for words in f:
        stopwords.append(words)
    final=[]
    for word in line:
        if word not in stopwords:
            final.append(word)
    finalString="".join(final)
    f.close()
    return finalString


lines=pd.read_csv("F:\\record.csv",encoding="GB2312")
lines=shuffle(lines)
comments=lines['comment']
for comment in comments:
    comment=remove_punctuation(comment,strip_all=False)
    comment=cutline(comment)
    comment=get_stopwords(comment)
    comments_new.append(comment)




tfidf_model=tfidf2.fit(comments_new)
#print(len(tfidf_model.vocabulary_))
result=tfidf_model.transform(comments_new)
#print(result.shape)
#print(comments_new[0])

classification=lines['classification']
print(len(classification))
X_train=result[0:140][:]
Y_train=classification[0:140][:]

X_test=result[141:][:]
Y_test=classification[141:][:]

####SVM
svm=svm.SVC(C=200)
svm.fit(X_train, Y_train)


###NB
clf = MultinomialNB()
clf.fit(X_train, Y_train)


####Logistic Regression
lr=LogisticRegression()
lr.fit(X_train,Y_train)

###dummy classifier
dummy_model=DummyClassifier()
dummy_model.fit(X_train,Y_train)
print("val mean accuracy: {0}".format(svm.score(X_test, Y_test)))
print("val mean accuracy: {0}".format(clf.score(X_test, Y_test)))

print("val mean accuracy: {0}".format(lr.score(X_test, Y_test)))

print("val mean accuracy: {0}".format(dummy_model.score(X_test, Y_test)))



