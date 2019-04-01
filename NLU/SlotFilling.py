import re

from NLU import IntentClassification
class SlotFiller:
    def __init__(self):
        pass
    @staticmethod
    def search( text, trigger_words, slot, slot_keys):
        count = 0
        if slot_keys == "tele":
            if len(re.findall(
                    r'[\u4E00-\u9FA5]*1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}[\u4E00-\u9FA5]*',
                    text)) != 0:
                text = re.compile(u'[\u4E00-\u9FA5.，,。？“”]+', re.UNICODE).sub("", text)
                slot['tele'] = text
                return True
            else:
                return False
        else:
            for item in trigger_words:
                if text.find(item) == -1:
                    count += 1
                    continue
                else:
                    if (slot_keys == "location"):
                        text = text[text.find("路") - 2:text.find("路") + 3]
                        slot[slot_keys] = text
                        break
                    elif (slot_keys == "failure"):
                        slot[slot_keys] = IntentClassification.IntentClassify.classify_failure(text)
                        break
                    elif (slot_keys == "brand"):
                        slot[slot_keys] = IntentClassification.IntentClassify.classify_brand(text)
                        break
                    elif (slot_keys == "version"):
                        slot[slot_keys] = IntentClassification.IntentClassify.classify_version(text)
                        break
                    else:
                        break
            if count == len(trigger_words):
                return False
        return True


