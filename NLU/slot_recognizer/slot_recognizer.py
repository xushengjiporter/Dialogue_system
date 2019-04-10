import static_variables,re


class SlotRecognizer:
    def __init__(self):
        pass

    def slot_recognizer(self,text,cf):
        ####recognize the slot keys
        slot_list = []
        if cf=='inform':
            if len(re.findall(
                    r'[\u4E00-\u9FA5]*1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}[\u4E00-\u9FA5]*',
                    text)) != 0:
                slot_list.append("tele")
            else:
                for slots_keys, slots_trigger_word in static_variables.REPLIES_DICT["trigger_dict"].items():
                    words_list = slots_trigger_word.split(",")
                    for words in words_list:
                        if words in text:
                            slot_list.append(slots_keys)
                            break
        elif cf=='request':
            a=static_variables.REPLIES_DICT["trigger_dict"].items()
            c=static_variables.REPLIES_DICT["trigger_request_dict"].items()
            for slots_keys, slots_trigger_word in static_variables.REPLIES_DICT["trigger_request_dict"].items():
                words_list = slots_trigger_word.split(",")
                for words in words_list:
                    if words in text:
                        slot_list.append(slots_keys)
                        break
        if len(slot_list)>0:
            return slot_list
        else:return False


    def recognize_failure(self,text):
        #####recognize the slot value

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

    def recognize_brand(self,text):
        #####recognize the slot value

        if ((text.find("海信") != -1)):
            classfication = "海信"
        elif ((text.find("科龙") != -1)):
            classfication = "科龙"

        return classfication

    def recognize_version(self,text):
        #####recognize the slot value


        if ((text.find("柜机") != -1)):
            classfication = "柜机"
        elif ((text.find("挂机") != -1)):
            classfication = "挂机"
        return classfication

    def recognize_tele(self,text):
        #####recognize the slot value
        if len(re.findall(
                r'[\u4E00-\u9FA5]*1((3[\d])|(4[75])|(5[^3|4])|(66)|(7[013678])|(8[\d])|(9[89]))\d{8}[\u4E00-\u9FA5]*',
                text)) != 0:
            tele = re.compile(u'[\u4E00-\u9FA5.，,。？“”]+', re.UNICODE).sub("", text)
            return tele
        else:return False

    def recognize_location(self,text):
        #####recognize the location value
        text = text[text.find("路") - 2:text.find("路") + 4]
        return text





