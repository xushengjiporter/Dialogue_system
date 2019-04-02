import datetime
from NLU import SlotFilling,IntentClassification

class PolicyLearningMapping:
    deny_flag = False
    deny_count = 0
    new_date = 0

    # def __init__(self):
    #     self.deny_flag = False
    #     self.deny_count = 0
    #     self.new_date = 0


    def process_time(self,text,replies_dict,sys_intent,new_slot,slot):
        if (("好的" in text) | ("行" in text) | ("可以" in text) | ("方便" in text)) & ("不" not in text):
            replies_dict["need_ask_slot"].remove("time")
            sys_intent.append(replies_dict["need_ask_slot"][0])
            new_slot["time"] = False
            if self.new_date == 0:
                self.new_date = (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H") + "点"
                slot["time"] = self.new_date
            else:
                slot["time"] = self.new_date

            return replies_dict["ending"]

        elif ("不好" in text) | ("不行" in text) | ("不可以" in text) | ("不方便" in text):
            if ( self.deny_flag is False) & ( self.deny_count < 2):
                self.deny_flag = True
                self.deny_count += 1
                hours = int((datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H"))
                if hours >= 13 & hours <= 24:
                    self.new_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + "10点"
                else:
                    self.new_date = (datetime.datetime.now() + datetime.timedelta(hours=5)).strftime("%Y-%m-%d %10") + "点"
                return "那您看{}行吗".format(self.new_date)
            elif (self.deny_flag is True) & (self.deny_count < 2):
                self.deny_count += 1
                return "请您提供合适的时间段，格式为xx年xx月xx日xx点(xx年xx月xx日上午/下午),例如2019年3月25日10点或者2019年3月25日上午/下午"
            elif self.deny_count >= 2:
                return "我找个同事帮帮你确认下时间吧，已经为您转接人工服务"

        elif ("年" in text) | ("月" in text) | ("日" in text):
            a = text[text.find("年") - 4]
            b = text.find("点")
            self.new_date = text[text.find("年") - 4:text.find("点") + 1]
            return "好的了解，帮您预约在{}行吗".format(self.new_date)
        else:
            return False

    def ask_slot(self,text,slot):
        if ("故障" in text)|("坏了" in text):
            return "您的空调故障信息为"+slot["failure"]
        elif ("品牌" in text)|("牌子" in text):
            return "您的空调品牌为为"+slot["brand"]
        elif ("产品型号" in text)|("型号" in text):
            return "您的空调型号信息为"+slot["version"]
        elif ("地址" in text)|("地址" in text):
            return "您的空调上门维修地址为"+slot["location"]
        elif ("时间" in text)|("预约时间" in text):
            return "您的空调预约时间为"+slot["time"]
        elif ("手机号码" in text)|("联系方式" in text)|("手机" in text):
            return "您的联系方式为"+slot["tele"]

    def book_maintainess(self,text,replies_dict,slot,slot_keys,new_slot,sys_intent):

        #if(SlotFilling.SlotFiller.search(text,IntentClassification.IntentClassify.replies_dict["trigger_dict"][slot_keys].split(","),IntentClassification.IntentClassify.slot,slot_keys) is True):
        if (SlotFilling.SlotFiller.search(text, replies_dict["trigger_dict"][
                slot_keys].split(","), slot, slot_keys) is True):

            if (len(replies_dict["need_ask_slot"]) >= 3) & (new_slot[slot_keys] is True):
                replies_dict["need_ask_slot"].remove(slot_keys)
                sys_intent.append(replies_dict["need_ask_slot"][0])
                new_slot[slot_keys] = False
                return_sentence = replies_dict["askings_dict"][sys_intent[-1]]
                if "{}" in return_sentence:
                    return_sentence = return_sentence.format(
                        (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H") + "点")
            elif (len(replies_dict["need_ask_slot"]) >= 2) & (new_slot[slot_keys] is False):
                    return_sentence = replies_dict["update_dict"][slot_keys] + "\n" + replies_dict["askings_dict"][
                        sys_intent[-1]]
                    if "{}" in return_sentence:
                        return_sentence = return_sentence.format(
                            (datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H") + "点")
            elif (len(replies_dict["need_ask_slot"]) == 2) & (new_slot[slot_keys] is True):
                    return_sentence = replies_dict["ending"]
            elif (len(replies_dict["need_ask_slot"]) == 1):
                    return_sentence = replies_dict["update_dict"][slot_keys]
            return return_sentence
        else:
                return False

