from  data import initial_data
import re
import datetime
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

