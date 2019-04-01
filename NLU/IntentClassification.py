from data import initial_data
import datetime
from Util import data_cleaning
from DM import PolicyLearning
from NLU import SlotFilling
from model import agent

class IntentClassify:
    replies_dict = initial_data.loading_replies()
    slot, sys_intent, usr_intent, ending_greeting, new_slot = initial_data.initial_variable()
    history = ".\history\\"
    policy_mapping = PolicyLearning.PolicyLearningMapping()
    # def __init__(self):
    #     self.replies_dict=initial_data.loading_replies()
    #     self.slot,self.sys_intent,self.usr_intent,self.ending_greeting,self.new_slot=initial_data.initial_variable()
    #     self.history=".\history\\"
    #     self.policy_mapping = PolicyLearning.PolicyLearningMapping()


    def Communicative_function(self,text):
        return_sentence = False
        if ("重新开始" in text) | ("重启" in text):
            agent.intent_classify.replies_dict=initial_data.loading_replies()
            agent.intent_classify.slot, agent.intent_classify.sys_intent, agent.intent_classify.usr_intent, agent.intent_classify.ending_greeting, agent.intent_classify.new_slot=initial_data.initial_variable()
            return "你好，我是海信客服，请问有什么帮您的？"
        if("查询" in text)|("告诉" in text ):
            return self.policy_mapping.ask_slot(text,self.slot)

        else:
            if self.sys_intent[-1] == "time":
                text = data_cleaning.clean_time_text(text)
                return_sentence =self.policy_mapping.process_time(text,self.replies_dict,self.sys_intent,self.new_slot,self.slot)

            else:
                for item in self.replies_dict["confirm_daily_talk_dict"].keys():
                    flag = self.daily_talk(text, item)
                    if flag is not False:
                        return_sentence = flag
                    else:
                        continue
                for item in self.replies_dict["askings_dict"].keys():
                    flag = self.policy_mapping.book_maintainess(text, item)
                    if flag is not False:
                        return_sentence = flag
                    else:
                        continue
                if return_sentence is False:
                    return_sentence = self.replies_dict["error_reply"]


        if "感谢" in return_sentence:
            log_name = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            path = self.history + log_name + ".txt"
            with open(path, "a", encoding="utf-8") as f:
                for key, value in self.slot.items():
                    f.write(key)
                    f.write(":")
                    f.write(value + "\n")
            f.close()

        return return_sentence


    def daily_talk(self,text,slot_daily_talk):
        talk_list = self.replies_dict["trigger_daily_talk_dict"][slot_daily_talk].split(",")
        for item in talk_list:
            if item in text:
                return self.replies_dict["confirm_daily_talk_dict"][slot_daily_talk]
        return False





    @staticmethod
    def classify_failure(text):
        if ((text.find("制冷") != -1) | (text.find("冷风") != -1) | (text.find("凉风") != -1)):
            classfication = "空调制冷效果不好"
        elif ((text.find("制热") != -1) | (text.find("热风") != -1) | (text.find("太冷了") != -1)):
            classfication = "空调制热效果不好"
        elif ((text.find("味") != -1) | (text.find("臭") != -1) | (text.find("流水") != -1)):
            classfication = "空调有异味"
        elif ((text.find("漏水") != -1) | (text.find("滴水") != -1) | (text.find("味道") != -1)):
            classfication = "空调滴水"
        else:
            classfication = "未知异常"

        return classfication

    @staticmethod
    def classify_brand(text):
        if ((text.find("海信") != -1)):
            classfication = "海信"
        if ((text.find("科龙") != -1)):
            classfication = "科龙"
        return classfication

    @staticmethod
    def classify_version(text):
        if ((text.find("柜机") != -1)):
            classfication = "柜机"
        if ((text.find("挂机") != -1)):
            classfication = "挂机"
        return classfication

