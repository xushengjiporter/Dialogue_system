from Util import data_cleaning
from NLU import IntentClassification
intent_classify=IntentClassification.IntentClassify()


def get_response(text):
    text=data_cleaning.remove_punctuation(text,strip_all=False)
    text=data_cleaning.get_stopwords(text)
    text=intent_classify.Communicative_function(text)
    #text = PolicyLearning.policy(text)
    print('\033[1;32m' + "槽信息填充情况：", intent_classify.slot, '\033[0m')
    print('\033[1;32m' + "上一轮对话意图：", intent_classify.usr_intent[-2], '\033[0m')
    print('\033[1;32m' + "当前对话意图：", intent_classify.usr_intent[-1], '\033[0m')

    return text