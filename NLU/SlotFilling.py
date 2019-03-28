
import re
from  data import initial_data
from NLU import intent_classify
replies_dict=initial_data.loading_replies()

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
                    initial_data.slot[slot_attribute] = intent_classify.classify_failure(text)
                    break
                elif (slot_attribute == "brand"):
                    initial_data.slot[slot_attribute] = intent_classify.classify_brand(text)
                    break
                elif (slot_attribute == "version"):
                    initial_data.slot[slot_attribute] = intent_classify.classify_version(text)
                    break
                else:
                    break
        if count == len(info_list):
            return False
    return True