import datetime

class PolicyLearningMapping:
    def __init__(self):
        self.deny_flag = False
        self.deny_count = 0
        self.new_date = 0
    # deny_flag = False
    # deny_count = 0
    # new_date = 0

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


