import datetime
import re
from  data import initial_data
replies_dict=initial_data.loading_replies()
deny_flag=False
deny_count=0
new_date=0

def process_time(text):
    global deny_flag,deny_count,new_date
    if (("好的" in text)|("行" in text)|("可以" in text)|("方便" in text))&("不" not in text):
        replies_dict["need_ask_slot"].remove("time")
        initial_data.sys_intent.append(replies_dict["need_ask_slot"][0])
        initial_data.new_slot["time"]=False
        if new_date==0:
            new_date=(datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H")+"点"
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

    elif ("上午" in text)|("下午" in text):
        new_date=str(text).replace("上午","10点")
        new_date = str(text).replace("下午", "16点")
        return "好的了解，帮您预约在{}行吗".format(new_date)

def classify_normal_intent(text, sys_intent, slot_attribute, replies_dict):
    new_slot=initial_data.new_slot
    if (search(text, replies_dict["trigger_dict"][slot_attribute].split(","), slot_attribute) is True):
        if (len(replies_dict["need_ask_slot"]) >= 3) & (new_slot[slot_attribute] is True):
            replies_dict["need_ask_slot"].remove(slot_attribute)
            sys_intent.append(replies_dict["need_ask_slot"][0])
            new_slot[slot_attribute] = False
            return_sentence = replies_dict["askings_dict"][sys_intent[-1]]
            if "{}" in return_sentence:
                return_sentence=return_sentence.format((datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H")+"点")
        elif (len(replies_dict["need_ask_slot"]) >= 2) & (new_slot[slot_attribute] is False):
            return_sentence = replies_dict["update_dict"][slot_attribute] + "\n" + replies_dict["askings_dict"][sys_intent[-1]]
            if "{}" in return_sentence:
                return_sentence=return_sentence.format((datetime.datetime.now()+datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H")+"点")
        elif (len(replies_dict["need_ask_slot"]) == 2) & (new_slot[slot_attribute] is True):
            return_sentence = replies_dict["ending"]
        elif (len(replies_dict["need_ask_slot"]) == 1):
            return_sentence = replies_dict["update_dict"][slot_attribute]
        return return_sentence
    else:
        return False

def classify_daily_talk_intent(text,slot_daily_talk,replies_dict):
    talk_list=replies_dict["trigger_daily_talk_dict"][slot_daily_talk].split(",")
    for item in talk_list:
        if item in text:
            return replies_dict["confirm_daily_talk_dict"][slot_daily_talk]
    return False


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


def classify_brand(text):
    if ((text.find("海信") != -1)):
        classfication = "海信"
    if ((text.find("科龙") != -1)):
        classfication = "科龙"
    return classfication


def classify_version(text):
    if ((text.find("柜机") != -1)):
        classfication = "柜机"
    if ((text.find("挂机") != -1)):
        classfication = "挂机"
    return classfication

def policy(text):
    return_sentence=False
    if initial_data.sys_intent[-1]=="time":
        return_sentence=process_time(text)
    else:
        for item in replies_dict["confirm_daily_talk_dict"].keys():
            flag = classify_daily_talk_intent(text, item, replies_dict)
            if flag is not False:
                return_sentence = flag
            else:
                continue
        for item in replies_dict["askings_dict"].keys():
            flag = classify_normal_intent(text, initial_data.sys_intent, item, replies_dict)
            if flag is not False:
                return_sentence = flag
            else:
                continue
        if return_sentence is False:
            return_sentence = replies_dict["error_reply"]

    return return_sentence

def search(text, info_list, slot_attribute):
    count = 0
    if slot_attribute == "tele":
        if len(re.findall(
                r'[\u4E00-\u9FA5]*1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}[\u4E00-\u9FA5]*',
                text)) != 0:
            text = re.compile(u'[\u4E00-\u9FA5.，,。？“”]+', re.UNICODE).sub("", text)
            initial_data.slot['tele'] = text
            return True
        else:
            return False
    else:
        for item in info_list:
            if text.find(item) == -1:
                count += 1
                continue
            else:
                if (slot_attribute == "location"):
                    text = text[text.find("路") - 2:text.find("路") + 3]
                    initial_data.slot[slot_attribute] = text
                    break
                elif (slot_attribute == "failure"):
                    initial_data.slot[slot_attribute] = classify_failure(text)
                    break
                elif (slot_attribute == "brand"):
                    initial_data.slot[slot_attribute] = classify_brand(text)
                    break
                elif (slot_attribute == "version"):
                    initial_data.slot[slot_attribute] = classify_version(text)
                    break
                else:
                    break
        if count == len(info_list):
            return False
    return True


def get_response(text):
    text = policy(text)
    print('\033[1;32m' + "槽信息填充情况：", initial_data.slot, '\033[0m')
    print('\033[1;32m' + "上一轮对话意图：", initial_data.usr_intent[-2], '\033[0m')
    print('\033[1;32m' + "当前对话意图：", initial_data.usr_intent[-1], '\033[0m')
    print(initial_data.sys_intent)
    return text