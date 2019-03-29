import datetime
from  data import initial_data
from Util import data_cleaning
from NLU import intent_classify
replies_dict=initial_data.loading_replies()
deny_flag=False
deny_count=0
new_date=0
history_path=".\history\\"

def process_time(text):
    global deny_flag,deny_count,new_date
    if (("好的" in text)|("行" in text)|("可以" in text)|("方便" in text))&("不" not in text):
        replies_dict["need_ask_slot"].remove("time")
        initial_data.sys_intent.append(replies_dict["need_ask_slot"][0])
        initial_data.new_slot["time"]=False
        if new_date==0:
            new_date=(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H")+"点"
            initial_data.slot["time"] = new_date
        else:
            initial_data.slot["time"]=new_date

        return replies_dict["ending"]

    elif("不好" in text)|("不行" in text)|("不可以" in text)|("不方便" in text):
        if (deny_flag is False)&(deny_count<2):
            deny_flag=True
            deny_count+=1
            hours = int((datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H"))
            if hours >= 13 & hours <= 24:
                new_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d ") + "10点"
            else:
                new_date = (datetime.datetime.now() + datetime.timedelta(hours=5)).strftime("%Y-%m-%d %10") + "点"
            return "那您看{}行吗".format(new_date)
        elif (deny_flag is True)&(deny_count<2):
            deny_count += 1
            return "请您提供合适的时间段，格式为xx年xx月xx日xx点(xx年xx月xx日上午/下午),例如2019年3月25日10点或者2019年3月25日上午/下午"
        elif deny_count>=2:
            return "我找个同事帮帮你确认下时间吧，已经为您转接人工服务"

    elif ("年" in text)|("月" in text)|("日" in text):
        a=text[text.find("年")-4]
        b=text.find("点")
        new_date=text[text.find("年")-4:text.find("点")+1]
        return "好的了解，帮您预约在{}行吗".format(new_date)
    else:return False



def policy(text):
    return_sentence=False
    if initial_data.sys_intent[-1]=="time":
        text=data_cleaning.clean_time_text(text)
        return_sentence=process_time(text)
    else:
        for item in replies_dict["confirm_daily_talk_dict"].keys():
            flag = intent_classify.classify_daily_talk_intent(text, item, replies_dict)
            if flag is not False:
                return_sentence = flag
            else:
                continue
        for item in replies_dict["askings_dict"].keys():
            flag = intent_classify.classify_normal_intent(text, initial_data.sys_intent, item, replies_dict)
            if flag is not False:
                return_sentence = flag
            else:
                continue
    if return_sentence is False:
        return_sentence = replies_dict["error_reply"]
    if "感谢" in return_sentence:
        log_name=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        path=history_path+log_name+".txt"
        with open(path,"a",encoding="utf-8") as f:
            for key,value in initial_data.slot.items():
                f.write(key)
                f.write(":")
                f.write(value+"\n")
        f.close()



    return return_sentence